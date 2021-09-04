###############################################
## Author: Marcos Vinicio Pereira - 6º BD
##
## Exemplos em https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/

import mariadb
import sys

rule_db = [ {   'percept'     : '1'
              , 'relation'    : '=='
              , 'action'      : 1
            },
            {   'percept'     : '2'
              , 'relation'    : '=='
              , 'action'      : 4
            }
          ]

def eval_rule(rule, percept):
    if eval(percept + rule['relation'] \
            + rule['percept']):
        return rule['action']
    else:
        return None

def rule_engine(rule_db, percept):
    actions = []
    for rule in rule_db:
      actions.append(eval_rule(rule,percept))
    return actions

#####################################################
# Conectando com o MariaDB
try:
    conn = mariadb.connect(
        user="iasys",
        password="123",
        host="127.0.0.1",
        port=3307,
        database="IA"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Cursor
cur = conn.cursor()

## Produto - Faz a pesquisa e imprime o Result-set
cur.execute("SELECT * FROM produto ORDER BY prd_id")
for ( item ) in cur:
    print(f"Produto: {item[0]}")
print("")

## Sugestões - Pesquisa e imprime
cur.execute("SELECT A.sug_prd_id \
                  , B.sco_prd_id \
             FROM sugerir A \
                  JOIN sugerir_comprado B ON A.sug_id = B.sug_id \
             ORDER BY A.sug_prd_id")

sugerido = ""
texto    = ""
primeiro = True
for ( item ) in cur:
    if sugerido != item[0]:
        sugerido = item[0]
        primeiro = True
        if texto != "":
            print(texto)
        texto = "Sugerir " + item[0] + " para opções "
    texto += ("" if primeiro else " + ") + item[1]
    primeiro = False

if texto != "":
    print(texto)
    

# Executando as regras

print( rule_engine(rule_db, '1') )
print( rule_engine(rule_db, '2') )
print( rule_engine(rule_db, '3') )  
    
