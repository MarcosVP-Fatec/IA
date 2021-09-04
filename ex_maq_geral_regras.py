# Author: Fabrício G. M. C - Ph.D
##

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

percept = '2'
print( rule_engine(rule_db, percept) )  
    
