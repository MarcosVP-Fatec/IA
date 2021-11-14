###############################################
## Author: Marcos Vinicio Pereira - 6º BD
##
## Exemplos em https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/

import os
from mariadb_connect import mariadb_connect_cursor
cur = mariadb_connect_cursor()

def ler_produtos():
    """
    :return: Lista de produtos por ordem alfabética.
    """
    cur.execute("SELECT P.prd_id FROM produto P ORDER BY P.prd_id")
    if cur is None:
        print()
        print("Não há produtos cadastrados!")
        return []

    produtos = []
    for linha in cur:
        produtos.append(linha[0])
    return produtos
    
# Retorna a sugestão conforme as regras
def printProducts(produtos):
    """
    Faz a impressão em tela da lista de produtos com código para seleção
    """
    n_proximo = 0
    n_total = len(produtos)
    colunas = 8
    largura = 12
    largura_src = '{:<'+str(largura)+'}'
    c_traco = "-" * ((8+largura) * colunas)
    os.system('cls')
    print(c_traco)
    print(" Itens para Compra")
    print(c_traco)
    quebra = ""
    n_add_cols = colunas - (len(produtos) % colunas)
    for item in produtos:
        n_item = n_proximo + 1
        quebra = "\n" if n_item % colunas == 0 else ""
        print( '{:>3}'.format(str(n_item)) , "-" , largura_src.format(item[:largura]) , "|", end = quebra )
        n_proximo += 1
    if n_add_cols > 0:
        quebra = ""
        largura_src = '{:<'+str(largura+6)+'}'
        for item in range(n_add_cols):
            print( largura_src.format("") , "|", end = quebra )    
    if quebra == "":
        print("")
    print(c_traco)
    return c_traco

def printPurchase( carrinho , produtos ):
    """
    Lista o que já foi comprado
    """
    if len(carrinho) > 0:
        c_texto = "Você já comprou: "
        print(c_texto,end="")
        primeiro = True
        for item in carrinho:
            print(" "*(0 if primeiro else len(c_texto)),carrinho[item], \
                  "["+'{:>2}'.format(str(produtos.index(item)+1))+"]", \
                  item )
            primeiro = False

def inputPurchase( texto , carrinho , already_suggested ):
    """
    Rotina que identifica o que foi comprado e retorna um dicionário com item e quantidade
    """
    comprado = input( texto ).replace(" ","").replace(".",",").split(",")
    comprado = [int(item) for item in comprado if item.isdigit() and 0 < int(item) < (len(produtos)+1)]
    if len(comprado) == 0:
        return []
    comprado.sort()
    n_qtd = 0
    for item in comprado:
        item = produtos[item-1]
        n_qtd = carrinho[item] + 1 if {item}.issubset(carrinho) else 1
        carrinho.update({item: n_qtd})
        if already_suggested.count(item) == 0:
            already_suggested.append(item)
    return len(comprado) > 0

def informar_lista_de_compra(produtos,sug_sugestao):
    """
    Digitar os códigos do que será comprado e retornar uma lista numérica de int
    """
    carrinho = dict()
    already_suggested = []

    os.system('cls')
    c_traco = printProducts(produtos)
    while True:    
        if not inputPurchase("Informe os códigos dos itens que quer comprar (separados por vírgula): ",carrinho,already_suggested):
            break
        os.system('cls')
        printProducts( produtos )
        printPurchase( carrinho , produtos )
        sugestoes = getSuggest(carrinho,suggest_bd,already_suggested, 2)
        print(c_traco)
        if len(sugestoes) > 0:
            print("Não esqueça de levar também: ",end="")
            separador = ""
            for item in sugestoes:
                print( separador + str(produtos.index(item)+1) + "-" + item , end = "")
                separador = " | "
            print()
        else:
            print("Deseja mais alguma coisa?")    
        print(c_traco)    
    return len(carrinho) > 0

def getSuggest(carrinho, suggest_bd, already_suggested, n_qtd_suggest=1):
    """
    Retorna uma lista de sugestões conforme quantidade solicitada
    Considera as sugestões já exibidas para não mostrar novamente.
    """
    sugs = []
    for item in carrinho:
        if n_qtd_suggest == 0: break
        if {item}.issubset(suggest_bd):
            for item_sugerido in suggest_bd[item]:
                if n_qtd_suggest == 0: break
                if sugs.count(item_sugerido) == 0 and already_suggested.count(item_sugerido) == 0 :
                    sugs.append(item_sugerido)
                    already_suggested.append(item_sugerido)
                    n_qtd_suggest -= 1
    return sugs

def ler_sugestoes():
    """
    Lê o banco de dados de sugestões e retorna um dicionário.
    """
    sugs = dict()

    cur.execute("SELECT sug_percept         \
                      , sug_sugestao        \
                      FROM sugerir          \
                      ORDER BY sug_percept  \
                             , sug_conf DESC")
    if not cur is None:
        c_last_item = ""
        for linha in cur:
            percept = linha[0]
            if not {percept}.issubset(sugs):
                sugs[percept] = []
            sugs[percept].append(linha[1])

    return sugs

###################################################################
# Executar as compras e ver sugestões
produtos = ler_produtos()
suggest_bd = ler_sugestoes()

while True:
    
    if len(produtos) == 0: break

    if not informar_lista_de_compra(produtos,suggest_bd):
        break

