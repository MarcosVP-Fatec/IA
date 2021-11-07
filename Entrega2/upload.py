##
# Função: Subir os dados do arquivo basket.csv para o banco de dados Maria DB
#
# Autor: Marcos Vinicio Pereira - Fatec BD - Período 6.
# Matéria Laboratório de Desenvolvimento de BD VI
# Professor: Fabrício G. M. de Carvalho, Ph.D
##

def adjustDateTime( datetime ):
    return datetime[6:10]  + "-" + \
           datetime[3:5]   + "-" + \
           datetime[0:2]   + " " + \
           datetime[11:16] + ":00"

from mariadb_connect import mariadb_connect_cursor
import csv
import os
import time    
time.strftime('%d-%m-%Y %H:%M:%S')

curpath = os.getcwd() + '\\Entrega2\\'

with open(curpath + 'basket.csv', 'r') as arqcsv:
    reader = csv.reader(arqcsv, delimiter=',', quoting=csv.QUOTE_NONE)
     
    ## Carregar o conjunto de produtos

    prods = set()
    vet_items = []
    ignore = True
    for linha in reader:
        if ignore:
            ignore = False
        else:    
            prods.add(linha[1])
            vet_items.append(linha)

    ## Conectando com o MariaDB
    cur = mariadb_connect_cursor()

    ### PRODUTOS
    ## Lendo e colocando em ordem
    vet_prods = []
    for linha in prods:
        vet_prods.append(linha)
    vet_prods.sort()

    ## Limpando o cadastro atual de transações
    cur.execute("DELETE FROM transacao")
    cur.execute("COMMIT")

    ## Limpando o cadastro atual de produtos
    cur.execute("DELETE FROM produto")
    cur.execute("COMMIT")
    
    ## Incluindo os produtos
    ## Estrutura da linha
    #  (0) Transaction
    #  (1) Item
    #  (2) date_time
    #  (3) period_day (afternoon, evening, morning, night)
    #  (4) weekday_weekend
    for n_linha in range(len(vet_prods)):
        novo = vet_prods[n_linha]
        print(novo)
        cur.execute("INSERT INTO produto (prd_id) \
                     VALUES (?)",(novo,))
    cur.execute("COMMIT")

    cur.execute("SELECT COUNT(*) FROM produto")
    print("====================================")
    print("TOTAL DE PRODUTOS       : " , cur.fetchall()[0][0])
    print("====================================")

    # Inserindo Transações
    reader = csv.reader(arqcsv, delimiter=',', quoting=csv.QUOTE_NONE)    
    for n_linha in range(len(vet_items)):
        cur.execute("INSERT INTO transacao ( tran_id \
                                           , tran_prod \
                                           , tran_date_time \
                                           , tran_period_day \
                                           , tran_week_day_end ) \
                     VALUES (?,?,?,?,?)", ( vet_items[n_linha][0] \
                                          , vet_items[n_linha][1] \
                                          , adjustDateTime(vet_items[n_linha][2]) \
                                          , vet_items[n_linha][3] \
                                          , vet_items[n_linha][4] ))
    cur.execute("COMMIT")

    cur.execute("SELECT COUNT(*) FROM transacao")
    print("TOTAL DE LINHAS GRAVADAS: " , cur.fetchall()[0][0])
    print("====================================")

    #n_tot_transact = 0
    # for (linha) in cur:
    #     n_tot_transact += linha[1]
    cur.execute("SELECT COUNT(X.tran_id) FROM (SELECT T.tran_id FROM transacao T GROUP BY T.tran_id) X")
    print("TOTAL DE TRANSAÇÕES     : " , cur.fetchall()[0][0])
    print("====================================")
    input("Tecle algo para fechar...")
    
arqcsv.close()

