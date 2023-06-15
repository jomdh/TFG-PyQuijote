
import itertools
import decimal
from pi_chudnovsky_bs import pi_chudnovsky_bs
from pathlib import Path
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

class PiEncoder:
    def __init__(self, text, n=None, archivo_precomp=None):
        """
        Inicializa una instancia de PiEncoder.
        Args:
            text (str): El texto que se va a codificar.
            n (int, optional): Valor explícito para n.
            archivo_precomp (str, optional): Ruta a un archivo con decimales precalculados de Pi.
        """
        self.text = text
        self.l = len(text)
        self.chars = set(text)
        self.n = n if n is not None else self.calculo_n_inicial()
        self.fragmentos = []
        self.mapping = {}
        self.df = pd.DataFrame()
        self.archivo_precomp = archivo_precomp

    def calculo_n_inicial(self):
        """
        Calcula el valor inicial de n, basado en la longitud del set de caracteres.
        """
        print ("el texto contiene %s caractereres, su set tiene %s caracteres unicos" % (self.l, len(self.chars)))
        print ("por tanto, el valor de n debe ser como minimo %s" % len(str(len(self.chars))))
        return len(str(len(self.chars)))

    def buscar_mapeo(self):
        """
        Busca un mapeo válido, generando fragmentos de Pi y mapeando los caracteres a estos fragmentos.
        """
        fin = False
        while not fin:
            print ("El texto contiene %s caracteres" % len(self.text))
            print("para n= %s, necesitamos %s decimales de pi." % (self.n, self.n * self.l))
            solucion = {}
            keys = self.generar_fragmentos()
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
    
    def cargar_datos_precomputados(self, archivo):
        """
        Carga decimales de Pi desde un archivo precomputado.
        Args:
            archivo (str): Ruta al archivo con los decimales precomputados de Pi.
        Returns:
            decimal.Decimal: Los decimales de Pi leídos del archivo o None si hubo algún error.
        """
        try:
            with open(archivo, "r") as file:
                print(f"Leyendo los primeros {self.n * self.l + 2} decimales de Pi desde '{archivo}'...")
                # Leer solo los decimales necesarios
                pi_decimals = file.read(self.n * self.l + 2)  # +2 to skip "3."
                pi = decimal.Decimal("0." + pi_decimals[2:])  # transform into decimal format, e.g., "0.1415..."
                print(f"Decimales de Pi cargados correctamente desde '{archivo}'")
                return pi
        except FileNotFoundError:
            print(f"No se encontró el archivo '{archivo}'")
            return None
        except ValueError:
            print(f"No se pudo convertir el contenido del archivo '{archivo}' a decimal")
            return None
    
    def generar_fragmentos(self):
        """
        Genera los fragmentos de Pi necesarios para el mapeo.
        Returns:
            list: Una lista de fragmentos de Pi.
        """
        # Verificar si se va a cargar Pi desde un archivo
        if self.archivo_precomp:
            print("Intentando cargar los decimales de Pi desde un archivo...")
            pi = self.cargar_datos_precomputados(self.archivo_precomp)
            if not pi:
                print("Cargando los decimales de Pi desde el algoritmo de Chudnovsky...")
                pi = pi_chudnovsky_bs(self.n * self.l)
        else:
            print("Cargando los decimales de Pi desde el algoritmo de Chudnovsky...")
            pi = pi_chudnovsky_bs(self.n * self.l)

        decimal.getcontext().prec = self.n * self.l
        # imprimimos los decimales de pi, sin la parte entera
        pi  = decimal.Decimal(pi) + 0

        print("Generando los fragmentos de Pi...")
        m = map(''.join, itertools.zip_longest(*[iter(str(pi)[2:])]*self.n, fillvalue=''))
        fragmentos = list(m)[:self.l]
        print("Fragmentos de Pi generados correctamente.")
        return fragmentos

    def generar_dataframe(self):
        """
        Genera un dataframe a partir del mapeo encontrado.
        """
        matrix = []
        for key, value in self.mapping.items():
            matrix.append([key, value])

        matrix.sort(key=lambda x: x[0])

        df = pd.DataFrame(matrix, columns=['key', 'value'])
        df = df.groupby('value').agg(lambda x: list(x)).reset_index()
        df['count'] = df['key'].apply(lambda x: len(x))
        df = df.sort_values(by='count', ascending=False)
        self.df = df
    
    def imprimir_dataframe(self):
        """
        Imprime el dataframe generado.
        """
        print(self.df)
        # save dataframe to csv
        df.to_csv('mapping.csv', index=False)

    def graficar_mapeo(self):
        """
        Genera una gráfica de barras a partir del dataframe.
        """
        if not self.df.empty:
            sns.set(style="whitegrid")
            sns.set(rc={'figure.figsize':(11.7,8.27)})
            ax = sns.barplot(x="count", y="value", data=self.df)
            ax.set(xlabel='Number of keys', ylabel='Value')
            plt.show()
        else:
            print("The dataframe is empty, and the plot cannot be generated.")

def main(archivo, start=0, end=0, n=None, archivo_precomp=None):
    """
    Función principal del programa.
    Args:
        archivo (str): Ruta al archivo con el texto a codificar.
        start (int): Índice de inicio del texto a codificar.
        end (int): Índice de fin del texto a codificar.
        n (int): Número de decimales de Pi a utilizar.
        archivo_precomp (str): Ruta al archivo con los decimales de Pi precomputados.
    """
    # Definimos la ruta del archivo
    ruta_archivo = Path(archivo)

    # Verificamos si el archivo existe
    if not ruta_archivo.exists():
        print(f"El archivo '{archivo}' no existe.")
        return

    # Leemos el contenido del archivo
    with open(ruta_archivo, 'r', encoding='utf-8-sig') as file:
        file_data = file.readlines()[start:-end or None]
    file_data = ''.join(file_data)

    # Creamos una instancia de PiEncoder con el texto del Quijote
    print("Creando una instancia de PiEncoder con el texto del Quijote...")
    mapper = PiEncoder(file_data, n, archivo_precomp)

    print("Buscando el mapeo óptimo...")
    mapper.buscar_mapeo()

    # Verificamos si el mapeo es óptimo
    if len(mapper.mapping) == len(file_data):
        print("No es una solución óptima")
    else:
        print("Se ha encontrado una solución óptima")

    # Generamos y mostramos el dataframe y la gráfica de distribución
    print("Generando el dataframe...")
    mapper.generar_dataframe()
    mapper.imprimir_dataframe()

    print("Mostrando la gráfica de distribución...")
    mapper.graficar_mapeo()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Interfaz de línea de comandos de PiEncoder")
    parser.add_argument("nombre_archivo", help="Ruta al archivo de texto de entrada")
    parser.add_argument("-s", "--inicio", type=int, default=0, help="Número de caracteres para saltar desde el principio del archivo")
    parser.add_argument("-e", "--final", type=int, default=0, help="Número de caracteres para saltar desde el final del archivo")
    parser.add_argument("-n", "--establecer-n", type=int, default=None, help="Establecer un valor explícito para n")
    parser.add_argument("-p", "--archivo-pi", type=str, default=None, help="Ruta a un archivo con decimales precalculados de Pi")
    argumentos = parser.parse_args()
    main(argumentos.nombre_archivo, argumentos.inicio, argumentos.final, argumentos.establecer_n, argumentos.archivo_pi)
