##
# Função: Análise "b" - Armazenamento das recomendações
#
# Autor: Marcos Vinicio Pereira - Fatec BD - Período 6.
# Matéria Laboratório de Desenvolvimento de BD VI
# Professor: Fabrício G. M. de Carvalho, Ph.D
#
# Fonte adaptado do original: Fabrício G. M. de Carvalho, Ph.D
###

import copy

#from apyori import apriori
from mariadb_connect import mariadb_connect_cursor

## Conectando com o MariaDB
cur = mariadb_connect_cursor()

#Support calculation
def support(Ix, Iy, bd):
    sup = 0
    key = list(Ix)[0]
    for transaction in bd:
        if (Ix.union(Iy)).issubset(transaction):
            sup += transaction[key]
    sup = sup/len(bd)
    return sup

# Confidence calculation
def confidence(Ix, Iy, bd):
    Ix_count = 0
    Ixy_count = 0
    keyX = list(Ix)[0]
    keyY = list(Iy)[0]
    for transaction in bd:
        if Ix.issubset(transaction):
            Ix_count += transaction[keyX]
            if (Ix.union(Iy)).issubset(transaction):
                Ixy_count += transaction[keyY]
    conf = Ixy_count / Ix_count
    return conf

# This function eliminates all the items in
# ass_rules which have sup < min_sup and
# conf < min_conf. It returns a "pruned" list
def prune(ass_rules, min_sup, min_conf):
    pruned_ass_rules = []
    for ar in ass_rules:
        if ar['support'] >= min_sup and ar['confidence'] >= min_conf:
            pruned_ass_rules.append(ar)
    return pruned_ass_rules

#####################################################################
# Gerar o vetor de itens
def itemSet():
    """
        1.Lê as transações direto no BD\n
        2.Gera um conjunto (SET) com todos os produtos\n
        :return: Lista de itens ordenados alfabeticamente
    """
    itemset = set()
    cur.execute("SELECT DISTINCT T.tran_prod FROM transacao T ORDER BY T.tran_prod")
    for ( linha ) in cur:
        itemset.add(linha[0])
    v_items = [item for item in itemset]
    v_items.sort()
    return v_items

#####################################################################
# Gerar o vetor de transações que conterá dicionários com quantidades
def transactionSet( transactions_bd ):
    """ 
    1. Lê todas as transações no BD por ordem de ID + Produto\n
    2. Agrupa por dicininário de itens e quantidades relacionadas
    """
    cur.execute("SELECT T.tran_id   \
                      , T.tran_prod \
                FROM transacao T    \
                ORDER BY T.tran_id, T.tran_prod")

    v_cur = cur.fetchall()
    dicionario = dict()
    n_len_transact = len(v_cur)
    n_lin_transact = -1
    n_transact = 0 
    FIELD_ID   = 0
    FIELD_PROD = 1
    while True:
        n_lin_transact += 1
        # Quando terminou de ter as transações grava o dicionario em memória
        if n_lin_transact == n_len_transact:
            if len(dicionario) > 0:
                transactions_bd.append(dicionario)
            break

        # Se mudou o código da transação grava o dicionario em memória
        if n_transact != v_cur[n_lin_transact][FIELD_ID]:
            n_transact = v_cur[n_lin_transact][FIELD_ID]
            if len(dicionario) > 0:
                transactions_bd.append(dicionario)
            dicionario = dict()

        item = v_cur[n_lin_transact][FIELD_PROD]
        dicionario[ item ] = dicionario[ item ] + 1 \
                             if {item}.issubset(dicionario) \
                             else 1
    return

# Grava o valor conforme a faixa
def gradient(grad,val):
    """
    Atualiza um vetor de Gradiente para contabilizar o número de ocorrência
    conforme a faixa em que ele se encontra.
    :param: grad: vetor de Gradiente que será alterado
    :param: val:  valor atual que será contabilizado no vetor de Gradiente
    """
    v_range = [0 , 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.8 , 0.9]
    for n in range(9,-1,-1):
        if val >= v_range[n]:
            grad[n] += 1
            break

# Imprime os gradientes
def print_gradient(texto,grad):
    """
    Impressão do Gradiente.
    Utilizado para Gradiente de Suporte ou de Confiança
    conforme a faixa em que ele se encontra.
    :param: grad: vetor de Gradiente que será alterado
    :param: val:  valor atual que será contabilizado no vetor de Gradiente
    """
    print('{:<19}'.format(texto) + ":" , ">= 0,9 -" , '{:>4}'.format(str(grad[9])) )
    for n in range(8,-1,-1):
        print('{:<19}'.format('') + " " , ">= 0,"+str(n)+" -" , '{:>4}'.format(str(grad[n])) )

# Adiciona as sugestões
def updateSuggestion(rules):
    """
    1.Exclui dados de SUGERIR\n
    2.Inclui as novas sugestões apuradas
    """

    # Exclui nates as recomendações atuais
    cur.execute("DELETE FROM sugerir")
    cur.execute("COMMIT")

    for rule in rules:
        print('Perception:' , '{:<20}'.format(rule['perception']) , end="")
        print('Suggestion:' , '{:<20}'.format(rule['suggestion']) )
        cur.execute("INSERT INTO sugerir (sug_percept, sug_sugestao, sug_sup, sug_conf) VALUES (?,?,?,?)" , \
                             (rule['perception'],rule['suggestion'],rule['support'],rule['confidence']))
    cur.execute("COMMIT")

# Apriori for association between 2 items
def apriori_2(itemset, bd, min_sup, min_conf, min_sup_item):
    """
    Executa o algoritmo apriori considerando grupos de dois items diferentes.
    :param: itemset: Lista de itens de produtos
    :param: bd: Lista de transações
    :param: min_sup: Suporte mínimo aceito
    :param: min_conf: Confiança mínima aceita
    conforme a faixa em que ele se encontra.
    :param: grad: vetor de Gradiente que será alterado
    :param: val:  valor atual que será contabilizado no vetor de Gradiente
    """
    if min_sup_item == None:
        min_sup_item = min_sup

    gradient_sup = [0,0,0,0,0,0,0,0,0,0]
    gradient_con = [0,0,0,0,0,0,0,0,0,0]
    ass_rules = []
    ass_rules.append([]) #level 1 (large itemsets)
    for item in itemset:
        sup = support({item},{item},bd)
        ass_rules[0].append({'rule': str(item), \
                             'support': sup, \
                             'confidence': 1})
        cur.execute("UPDATE produto SET prd_sup = ? WHERE prd_id = ?" \
                    ,(sup,item,))
    cur.execute("COMMIT")
    ass_rules[0] = prune(ass_rules[0], min_sup_item, min_conf)
    n_faltam = len(ass_rules[0]) ** 2
    print("Faltam ",n_faltam,end="")
    ass_rules.append([]) #level 2 (2 items association)
    for item_1 in ass_rules[0]:
        for item_2 in ass_rules[0]:
            if n_faltam % 1000 == 0:
                print(",", n_faltam,end="")
            n_faltam -= 1                

            if item_1['rule'] != item_2['rule']:
                #rule = item_1['rule'] + '_' + item_2['rule']
                Ix = {item_1['rule']}
                Iy = {item_2['rule']}
                sup = support(Ix, Iy, bd)
                conf = confidence(Ix, Iy, bd)
                gradient(gradient_sup,sup)
                gradient(gradient_con,conf)
                ass_rules[1].append({'perception': item_1['rule'], \
                                     'suggestion': item_2['rule'], \
                                     'support': sup, \
                                     'confidence': conf})

    ass_rules[1] = prune(ass_rules[1],min_sup, min_conf)
    ass_rules.append( {'gradient_sup': gradient_sup, 'gradient_con': gradient_con} )
    print(",", 0)
    return ass_rules

############################################################################################################
def run_apriori(n_minimal_support = 0.4 , n_minimal_confidence = 0.7 , n_minimal_support_unike = None):

    """
    Executa a aplicação apriori
    """
    print("-----------------------------------------------------------")
    print("Início da apuração das recomendações.")

    # Verifica se existem dados
    cur.execute("SELECT COUNT(*) AS QTD FROM produto")
    if cur.fetchall()[0][0] == 0:
        print('Não há produtos cadastrados!')
        return

    # define os repositórios dos dados
    print(">> Lista de itens... ",end="")
    itemset = itemSet()
    print("Total: " , len(itemset))

    # define as transações
    print(">> Transações...",end="")
    transactions_bd = []
    transactionSet(transactions_bd)
    print(".... Total: " , len(transactions_bd))

    # recomendações
    print("Apurando recomendações... ",end="")
    rules = apriori_2(itemset, \
                      transactions_bd, \
                      n_minimal_support, \
                      n_minimal_confidence, \
                      n_minimal_support_unike )
    print("Total de recomendações: " , len(rules[1]) , "| Suporte mínimo:", n_minimal_support, "| Confiança mínima:" , n_minimal_confidence)

    print_gradient("Gradient Support"   , rules[2]['gradient_sup'] )
    print("")
    print_gradient("Gradient Confidence", rules[2]['gradient_con'] )

    # Adiciona as sugestões
    print("Adicionando sugestões...")
    updateSuggestion(rules[1])

run_apriori( 0.01 / 100 , 50  / 100 ) 