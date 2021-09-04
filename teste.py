meu_dicionario = {'1' : 'Fabio', '2' : 'Maria', '3' : 'João', '4' : 'José'}

meu_dicionario['5'] = 'Joaquina'
print(meu_dicionario)

meu_dicionario.update({'6': 'Pedro'})
print(meu_dicionario)

print(meu_dicionario.get('1'))
print(meu_dicionario.get('7') is None)

vetor = ["AAA","BBB"]
if "AAAA" in vetor:
    print("sim")
else:
    print("não")

print("===========")
print("A" in "AA")
