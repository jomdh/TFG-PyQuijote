import functools
import itertools
import decimal
from implementations.chudnovsky_altorendimiento import pi_chudnovsky_bs
from pathlib import Path
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class PiTextMapper:
    def __init__(self, text, n=None):
        self.text = text
        self.l = len(text)
        self.chars = set(text)
        self.n = n if n is not None else self.calc_initial_n()
        self.chunks = []
        self.mapping = {}
        self.df = pd.DataFrame()

    def calc_initial_n(self):
        print ("el texto contiene %s caractereres, su alfabeto tiene %s caracteres unicos" % (self.l, len(self.chars)))
        print ("por tanto, el valor de n debe ser como minimo %s" % len(str(len(self.chars))))
        return len(str(len(self.chars)))


    def find_mapping(self):
        fin = False
        while not fin:
            print ("El texto contiene %s caracteres" % len(self.text))
            print("para n= %s, necesitamos %s decimales de pi." % (self.n, self.n * self.l))
            solucion = {}
            keys = self.generate_pi_chunks()
            #timer
            start = time.time()
            #loop principal
            fin = True
            for i, key in enumerate(keys):
                if key not in solucion:
                    solucion[key] = self.text[i]
                else:
                    if solucion[key] == self.text[i]:
                        continue
                    else:
                        print ('n= %s no es una solución válida' % self.n)
                        self.n = self.n + 1
                        fin = False
                        end = time.time()
                        print( 'F tiempo: %s' % (end - start))
                        break
        end = time.time()
        print ('n= %s SI una solución válida' % self.n)
        print( 'OK tiempo: %s' % (end - start))
        self.mapping = solucion
        
    
    def generate_pi_chunks(self):
        pi = pi_chudnovsky_bs(self.n * self.l)
        decimal.getcontext().prec = self.n * self.l
        # imprimimos los decimales de pi, sin la parte entera
        pi  = decimal.Decimal(pi) + 0

        m = map(''.join, itertools.zip_longest(*[iter(str(pi)[2:])]*self.n, fillvalue=''))
        return list(m)[:self.l]
    
    def generate_dataframe(self):
        matrix = []
        for key, value in self.mapping.items():
            matrix.append([key, value])

        matrix.sort(key=lambda x: x[0])

        df = pd.DataFrame(matrix, columns=['key', 'value'])
        df = df.groupby('value').agg(lambda x: list(x)).reset_index()
        df['count'] = df['key'].apply(lambda x: len(x))
        df = df.sort_values(by='count', ascending=False)
        self.df = df
    
    def print_dataframe(self):
        print(self.df)

    def plot_mapping(self):

        if not self.df.empty:
            sns.set(style="whitegrid")
            sns.set(rc={'figure.figsize':(11.7,8.27)})
            ax = sns.barplot(x="count", y="value", data=self.df)
            ax.set(xlabel='Number of keys', ylabel='Value')
            plt.show()
        else:
            print("The dataframe is empty, and the plot cannot be generated.")


import argparse

def main(filename, start=0, end=0, n=None):
    # Definimos la ruta del archivo
    file_path = Path(filename)

    # Verificamos si el archivo existe
    if not file_path.exists():
        print(f"El archivo '{filename}' no existe.")
        return

    # Leemos el contenido del archivo
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        file_data = file.readlines()[start:-end or None]
    file_data = ''.join(file_data)

    # Creamos una instancia de PiTextMapper con el texto del Quijote
    print("Creando una instancia de PiTextMapper con el texto del Quijote...")
    mapper = PiTextMapper(file_data, n)


    print("Buscando el mapeo óptimo...")
    mapper.find_mapping()

    # Verificamos si el mapeo es óptimo
    if len(mapper.mapping) == len(file_data):
        print("No es una solución óptima")
    else:
        print("Se ha encontrado una solución óptima")

    # Generamos y mostramos el dataframe y la gráfica de distribución
    print("Generando el dataframe...")
    mapper.generate_dataframe()
    mapper.print_dataframe()

    print("Mostrando la gráfica de distribución...")
    mapper.plot_mapping()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PiTextMapper CLI")
    parser.add_argument("filename", help="Path to the input text file")
    parser.add_argument("-s", "--start", type=int, default=0, help="Number of characters to skip from the beginning of the file")
    parser.add_argument("-e", "--end", type=int, default=0, help="Number of characters to skip from the end of the file")
    parser.add_argument("-n", "--set-n", type=int, default=None, help="Set an explicit value for n")

    args = parser.parse_args()
    main(args.filename, args.start, args.end, args.set_n)
