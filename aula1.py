#from modulo1 import proSoma
import modulo1 as nd

### comentario 

print("Aula de python")
print(__name__)


print(nd.proSoma(20,20))

# tratamento de exceções 

a = [1,2,3,4]
try:
    for i in range(6):
        print(a[i])
except IndexError:
    print ("Posicao inexistente {i}")
finally: 
    print("fim do try") 

#abrindo e lendo arquivos em phyton
arq = open('texto,txt', 'r')
for linha in arq:
    print(linha)
arq.close()

import json

ds404 = {'classe':"vespertino", 'nome': 'Top Sis Emb'}
print(ds404)

to_json = json.dumps(ds404)
print(to_json)
argW = open('toJson.txt', 'w')
argW.write(to_json)
argW.close()

#trabalhando com threads

import _thread
import time

def testeThread(a,b):
    print("Thread")
    for i in range(5):
        print(a*i)
        time.sleep(300)

val1 = 10
val2 = 20
_thread.start_new_thread(testeThread,(10,20))
print("terminou")