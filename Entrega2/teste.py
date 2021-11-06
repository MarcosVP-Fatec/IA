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

    cur.execute("SELECT * AS QTD FROM PRODUTO")
    print(cur.fetchone())
    print(cur.fetchall()[0][0])

arqcsv.close()

