#!/usr/bin/env python
# coding: utf-8


# importamos las librerías necesarias

import time
import pandas as pd
from pathlib import Path
import itertools
from textwrap import wrap

import decimal
# importamos el algoritmo de Chudnovsky de implementations/chudnovsky_altorendimiento.py
from implementations.chudnovsky_altorendimiento import pi_chudnovsky_bs



# importamos el archivo de texto del Quijote de la web de Gutenberg
# !python -m wget  https://www.gutenberg.org/cache/epub/2000/pg2000.txt

# definimos la ruta del archivo
recursos = Path.cwd() / "recursos"

quijote_file = recursos / 'primer_capitulo.txt'
quijote_file.exists()




# sea k el número de dígitos de precisión que se quieren calcular.
# este valor debe ser como máximo, el producto de n y el número total de caracteres del texto.

# por ejemplo, si n = 2, y el texto tiene 1000 caracteres, k = 2000.
# calcularemos el numero total de caracteres del texto

# abrimos el quijote como utf-8-sig, para evitar errores de codificación.    
with open(quijote_file, 'r', encoding='utf-8-sig') as file:
    # omitimos el copyright y los metadatos, para quedarnos solo con el texto íntegro de la obra.
    # leemos despues del caracter 27 hasta la línea -372.
    quijote_data = file.readlines()[36:-372]

# unimos todas las líneas en una sola cadena de texto.
quijote_data = ''.join(quijote_data)

# contamos los caracteres unicos del texto
caracteres = set(quijote_data)
# imprimimos los caracteres unicos
print(caracteres)
# imprimimos el número de caracteres unicos
print(len(caracteres))

# longitud en caracteres del texto
l = len(quijote_data)
print(l)




# longitud en caracteres de cada trozo de pi. como minimo dos, 
# ya que el alfabeto y todos los caracteres imprimibles pueden rondar los 100

# por tanto, n será como minimo, el valor del orden de magnitud superior de n.

print ("el texto contiene %s caractereres, su alfabeto tiene %s caracteres unicos" % (l, len(caracteres)))
print ("por tanto, el valor de n debe ser como minimo %s" % len(str(len(caracteres))))
n = len(str(len(caracteres)))

# de encontrar una solución con esta longitud, estaríamos muy cerca de la solución optima.
# si no se encuentra una solución, se incrementa el valor de n en 1 y se vuelve a intentar.
# si se encuentra una solución, se imprime el valor de n y el tiempo que ha tardado en encontrarla.





# tenemos ya por tanto, una estimación del numero de decimales de pi que necesitamos 
# para nuestra primera aproximación.

print ("decimales de pi necesarios = n * l = %s * %s = %s" % (n, l, n*l))

# por conveniencia, redondeamos el valor de n*l al siguiente valor dentro del orden de magnitud.
# para ello primero calculamos el log10 de n*l, y luego redondeamos hacia abajo.

# calculamos el log10 de n*l
log10 = decimal.Decimal(n*l).log10()
# redondeamos hacia abajo, quedandonos con el valor entero, para obtener el orden de magnitud.
exp = int(log10)

# calculamos el valor de k
k = int(n*l / 10**exp) + 1
k_r =(k * 10**exp)
print ("redondeado = %s" % k_r)







# generamos esa misma cantidad de decimales de pi
# para ello, usamos el algoritmo de Chudnovsky, que hemos importado al principio del notebook.

pi = pi_chudnovsky_bs(k_r)

decimal.getcontext().prec = k_r
# imprimimos los decimales de pi, sin la parte entera
pi  = decimal.Decimal(pi) + 0









# mapeamos los decimales de pi en trozos de n-elementos
# itertools.zip_longest se encarga de los impares sueltos

start = time.time()
# 
b = map(''.join, itertools.zip_longest(*[iter(str(pi)[2:])]*n, fillvalue=''))
end = time.time()
print(end - start)

# imprimimos los trozos de pi
# print (list(b))





# tantos trozos de pi como caracteres totales en texto
nlist = list(b)[:l]
# print(nlist)





# búsqueda: intenta crear un diccionario key:value en el que todo key sea único.
# si no lo consigue, sale del bucle.
# esta es una versión académica, pero se puede hacer más elegante.

res2 = {}
i=0
for key in nlist:
    if not key in res2:
        res2[key] = quijote_data[i]
    else:
        if res2[key] == quijote_data[i]:
            continue
        else:
            print ('not valid')
            break
    i = i+1





res2





len(res2)





# todo junto hasta que lo encuentre:

def map_pi(n,l):
    pi = pi_chudnovsky_bs(n * l)

    decimal.getcontext().prec = n * l
    # imprimimos los decimales de pi, sin la parte entera
    pi  = decimal.Decimal(pi) + 0

    m = map(''.join, itertools.zip_longest(*[iter(str(pi)[2:])]*n, fillvalue=''))
    return list(m)[:l]





#loop
def busca_solucion(n, text):
    fin = False
    while not fin:
        print ("El texto contiene %s caracteres" % len(text))
        print("para n= %s" % n)
        solucion = {}
        keys = map_pi(n,len(text))
        #timer
        start = time.time()
        #loop principal
        fin = True
        for i, key in enumerate(keys):
            if not key in solucion:
                solucion[key] = text[i]
            else:
                if solucion[key] == text[i]:
                    continue
                else:
                    print ('n= %s no es una solución válida' % n)
                    n = n+1
                    fin = False
                    end = time.time()
                    print( 'F tiempo: %s' % (end - start))
                    break
    end = time.time()
    print ('n= %s SI una solución válida' % n)
    print( 'OK tiempo: %s' % (end - start))
    return solucion

    





n=2 # valor inicial de n
solucion = busca_solucion(n, quijote_data)

if len(solucion) == len(quijote_data):
    print ("no es una solución óptima")





# create a matrix with the solution, with the values of the dictionary
# and the keys of the dictionary, sorted by value

matrix = []
for key, value in solucion.items():
    matrix.append([key, value])

matrix.sort(key=lambda x: x[0])

# import matrix into a dataframe
import pandas as pd

df = pd.DataFrame(matrix, columns=['key', 'value'])
# group by value, and concatenate the keys into an array
df = df.groupby('value').agg(lambda x: list(x)).reset_index()
# count the number of keys in each array
df['count'] = df['key'].apply(lambda x: len(x))
# sort by count
df = df.sort_values(by='count', ascending=False)
df





# plot the distribution of the number of keys in each array
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")
sns.set(rc={'figure.figsize':(11.7,8.27)})
ax = sns.barplot(x="count", y="value", data=df)
ax.set(xlabel='Number of keys', ylabel='Value')
plt.show()

