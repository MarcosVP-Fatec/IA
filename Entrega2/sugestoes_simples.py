###############################################
## Author: Marcos Vinicio Pereira - 6º BD
##
## Exemplos em https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/

from mariadb_connect import mariadb_connect_cursor

def ler_bd():

    # Conectando com o MariaDB - Pegando o cursor
    cur = mariadb_connect_cursor()
    # Sugestões - Pesquisa e imprime + adiciona itens ao vetor de dados
    cur.execute("SELECT A.sug_percept  \
                      , A.sug_sugestao \
                 FROM sugerir A      \
                 ORDER BY A.sug_percept, A.sug_sugestao")

    regras    = []

    for ( item ) in cur:

        regras.append( { "percept" : item[0]                        \
                       , "relation": " == "                         \
                       , "action"  : item[1]                        })

    return regras
    
rule_db = ler_bd()

# Retorna a sugestão conforme as regras
def eval_rule(rule, percept):
    if eval("'" + percept + "'" + rule['relation'] + "'" + rule['percept'] + "'"):
        return rule['action']
    else:
        return None

def rule_engine(rule_db, percept):
    sugestao = ""
    for rule in rule_db:
        sugestao = eval_rule(rule,percept)
        if sugestao is not None:
            break
        
    return "" if sugestao is None else sugestao

def jah_existe(rule, percept):
    for ( key ) in rule:
        if key["percept"] == percept:
            return True
    return False

###################################################################
# Permite incluir novas regras
def incluir_regras():
    while True:
        rule_db = ler_bd()
        novaregra = input("Informe o que foi comprado para nova regra: ").replace(" ","")
        if novaregra == "":
            break
        
        novaregra = novaregra.split(',')
        novaregra.sort()
        novaregra = ",".join( novaregra )

        if jah_existe(rule_db, novaregra):
            print("Regra já existe : " + novaregra)
        else:
            novasugestao = input("Informe a sugestão: ")
            if novasugestao != "":
                cur = mariadb_connect_cursor()
                for ( novo ) in novaregra.split():
                    cur.execute("SELECT COUNT(*)      \
                                 FROM produto P       \
                                 WHERE P.prd_id = ?"  , \
                                 (novo,))

                    if cur is not None:
                        for ( item ) in cur:
                            if item[0] == 0:
                                cur.execute("INSERT INTO produto (prd_id) \
                                               VALUES (?)" , \
                                            (novo,))
                                cur.execute("COMMIT")
                            break

                    cur.execute("SELECT COUNT(*)      \
                                 FROM produto P       \
                                 WHERE P.prd_id = ?"  , \
                                 (novo,))

                #Insere a sugestão no produto
                cur.execute("SELECT COUNT(*)      \
                             FROM produto P       \
                             WHERE P.prd_id = ?"  , \
                             (novasugestao,))
                if cur is not None:
                   for ( item ) in cur:
                       if item[0] == 0:
                          cur.execute("INSERT INTO produto (prd_id) \
                                       VALUES (?)" , \
                                       (novasugestao,))
                          cur.execute("COMMIT")
                          break

                #insere a sugestâo
                cur.execute("INSERT INTO sugerir        \
                             (sug_percept, sug_sugestao) VALUES (?,?)" , \
                             (novaregra,novasugestao,))
                                
                cur.execute("COMMIT")


###################################################################
# Informar o que foi comprado e exigir a sugestão

def informar_compra():
    while True:
        comprado = input("Informe o que foi comprado: ").replace(" ","")
        if comprado == "":
            break

        comprado = comprado.split(',')
        comprado.sort()
        comprado = ",".join( comprado )

        sugestao = rule_engine(rule_db, comprado)
        if sugestao != '':
            print("  Não se esqueça de comprar " + sugestao )
        

###################################################################
# Verificando o que irá rodar
while True:
    opc = input("Selecione 1-Incluir Regras, 2-Informar compra: ")
    if opc == '1':
        incluir_regras()
        rule_db = ler_bd()
    elif opc == '2':
        informar_compra()
    elif opc == '':
        break
    else:
        print("Opção inválida: " + opc)


