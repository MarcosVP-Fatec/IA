##
# Função: Análise "b" - Quantidades vendidas de cada unidade
#
# Autor: Marcos Vinicio Pereira - Fatec BD - Período 6.
# Matéria Laboratório de Desenvolvimento de BD VI
# Professor: Fabrício G. M. de Carvalho, Ph.D
##
import pandas as pd
import matplotlib.pyplot as plt
from mariadb_connect import mariadb_connect_cursor

def ChoiceNumber( texto , valorMaximo):
    n_opc = input(texto)
    if n_opc == "":
        return 0
    n_opc = int(n_opc)
    return min(n_opc,valorMaximo)

## Conectando com o MariaDB
cur = mariadb_connect_cursor()

## Definindo número de linhas que serão exibidas no gráfico
n_limit = input("Linhas a exibir: ")
if n_limit == "":
    n_limit = 100000
else:
    n_limit = int(n_limit)

if n_limit == 0:
    n_limit = 1000000

# Definindo período que será filtrado
cur.execute("SELECT DISTINCT T.tran_period_day \
             FROM transacao T \
             ORDER BY T.tran_period_day")
print("----------------------")
print("Períodos cadastrados")
periodos = []             
count = 1
print(0,"- TODOS")
for ( linha ) in cur:
    periodos.append(linha[0])
    print(count,"-",linha[0])
    count += 1
n_opc = ChoiceNumber("Número do período: ",len(periodos))
filter_period = periodos[n_opc-1] if n_opc > 0 else ""

## Lendo todas as transações
sql = "SELECT T.tran_prod, count(*) as QTD \
       FROM transacao T "
if filter_period != "":       
    if filter_period == "evening" or filter_period == "night":
        sql += "WHERE (T.tran_period_day = 'evening' OR T.tran_period_day = 'night') "
    else:     
        sql += "WHERE T.tran_period_day = '" + filter_period + "' "

sql += "GROUP BY T.tran_prod \
        ORDER BY count(*) DESC, T.tran_prod"

cur.execute(sql)

prods = []
quant = []
c_title = "Quantidades de Produtos Vendidos"
if filter_period != "":
    if filter_period == "evening" or filter_period == "night":
        c_title += "\nFiltro - Período de Venda: evening and night"
    else:
        c_title += "\nFiltro - Período de Venda: " + filter_period
c_title += "" if n_limit == 0 or n_limit > 10000 else ("\nLimitado às primeiras " + str(n_limit) + " maiores quantidades")
plt.title(c_title)
#plt.figure(figsize=(20,20))
count = 1
if cur is not None:
    for ( linha ) in cur:
        prods.append(linha[0])
        quant.append(linha[1])
        count += 1
        if count > n_limit:
            break
df = pd.DataFrame({'prods': prods,
                   'quant': quant}) 

df = df.sort_values(by=['quant'], ascending=True)

plt.barh(df['prods'],df['quant'],color='blue')
print("Exibindo gráfico...")
plt.show()




