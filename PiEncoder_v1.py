
"""
PiEncoder es un script en Python que codifica un texto dado en códigos numéricos utilizando los lugares decimales de π.

La clase principal de este módulo, PiEncoder, toma un texto y genera una codificación basada en los lugares decimales de π. El algoritmo de Chudnovsky se utiliza para generar los dígitos necesarios de π. 

Además de generar los dígitos de π en tiempo de ejecución, este módulo también ofrece la posibilidad de cargar los decimales de π desde un archivo con decimales pre-computados. Esto proporciona una alternativa eficiente al cálculo de los decimales de π, ya que los usuarios pueden simplemente descargar una tabla pre-computada de decimales de π de la web y usarla para codificar su texto.

El módulo también incluye una función `main` que permite usar la funcionalidad de PiEncoder desde la línea de comandos. Los usuarios pueden especificar el texto a codificar, el número de decimales de π a usar y la ruta a un archivo con los decimales pre-computados de π.
"""
__author__ = "Joaquin Martinez"
__version__ = "1.0"
__license__ = "GPL3"

import itertools
import decimal
from pi_chudnovsky_bs import pi_chudnovsky_bs
from pathlib import Path
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import math


class PiEncoder:
    def __init__(self, text, n=None, archivo_precomp=None):
        """
        Inicializa una instancia de PiEncoder.

        :param text: El texto que se va a codificar.
        :type text: str
        :param n: Valor explícito para n.
        :type n: int, optional
        :param archivo_precomp: Ruta a un archivo con decimales precalculados de Pi.
        :type archivo_precomp: str, optional
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
        print ("el texto contiene %s caractereres, \nsu charset tiene %s caracteres unicos" % (self.l, len(self.chars)))
        print ("por tanto, el valor de n debe ser su orden superior, es decir %s caracteres" % len(str(len(self.chars))))
        return len(str(len(self.chars)))

    def buscar_mapeo(self):
        """
        Busca un mapeo válido, generando fragmentos de Pi y mapeando los caracteres a estos fragmentos.

        Una vez que se encuentra un mapeo válido, se almacena en el atributo `mapping` del objeto PiEncoder. 

        Si no se encuentra un mapeo válido, el método incrementa el valor de `n` y vuelve a intentarlo.
        """
        fin = False
        while not fin:
            print("[ ] ============================================")
            print("[i] Para n= %s, necesitamos %s decimales de pi." % (self.n, self.n * self.l))
            solucion = {}
            keys = self.generar_fragmentos()
            #loop principal
            fin = True
            for i, key in enumerate(keys):
                if key not in solucion:
                    solucion[key] = self.text[i]
                else:
                    if solucion[key] == self.text[i]:
                        continue
                    else:
                        print ('[-] n= %s no es una solución válida' % self.n)
                        self.n = self.n + 1
                        fin = False
                        break
        print ('[i] Conseguido! para n= %s SI una solución válida' % self.n)
        self.mapping = solucion
    
    def cargar_datos_precomputados(self, archivo):
        """
        Carga los decimales de Pi desde un archivo precomputado.

        Este método intenta abrir un archivo dado y lee los primeros `self.n * self.l + 2` decimales de Pi.
        En caso de error, este método devuelve None y muestra un mensaje de error correspondiente.

        Args:
            archivo (str): Ruta al archivo que contiene los decimales precomputados de Pi.

        Returns:
            decimal.Decimal: Los decimales de Pi leídos del archivo, o None si hubo algún error.
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

        Este método primero verifica si hay un archivo de decimales precomputados de Pi disponible.
        Si el archivo está disponible, se intenta cargar los decimales de Pi desde este archivo.
        Si el archivo no está disponible o si hay un error al leer el archivo, se utilizan los decimales de Pi
        generados por el algoritmo de Chudnovsky.

        Returns:
            list: Una lista de fragmentos de Pi generados a partir de los decimales de Pi.
        """
        # Verificar si se va a cargar Pi desde un archivo
        if self.archivo_precomp:
            print("[ ] Intentando cargar los decimales de Pi desde un archivo...")
            pi = self.cargar_datos_precomputados(self.archivo_precomp)
            if not pi:
                print("[E] Carga Fallida. Cargando los decimales de Pi desde el algoritmo de Chudnovsky...")
                pi = pi_chudnovsky_bs(self.n * self.l)
        else:
            print("[ ] Cargando los decimales de Pi desde el algoritmo de Chudnovsky...")
            # timer
            start = time.time()
            pi = pi_chudnovsky_bs(self.n * self.l)
            end = time.time()
            print( '[i] Tiempo de ejecución del algoritmo: %s s.' % round(end - start, 3))


        decimal.getcontext().prec = self.n * self.l
        # imprimimos los decimales de pi, sin la parte entera
        pi  = decimal.Decimal(pi) + 0

        # print("[i] Generando los fragmentos de Pi...")
        m = map(''.join, itertools.zip_longest(*[iter(str(pi)[2:])]*self.n, fillvalue=''))
        fragmentos = list(m)[:self.l]
        # print("[i] Fragmentos de Pi generados correctamente.")
        return fragmentos

    def generar_dataframe(self):
        """
        Genera un dataframe a partir del mapeo encontrado.

        Este método transforma el mapeo en una matriz y luego genera un DataFrame a partir de esta matriz.
        El DataFrame se agrupa por el valor de los mapeos y se ordena por la cantidad de claves correspondientes a cada valor.
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
        Imprime el dataframe generado y lo guarda como archivo CSV.

        Este método muestra el DataFrame generado por `generar_dataframe` y lo guarda como archivo CSV con el nombre 'mapping.csv'.
        """
        print(self.df)
        # save dataframe to csv
        self.df.to_csv('mapping.csv', index=False)

    def graficar_mapeo(self):
        """
        Genera una gráfica de barras a partir del dataframe.

        Este método genera una gráfica de barras que muestra la distribución de los valores en el DataFrame.
        La gráfica se genera solo si el DataFrame no está vacío. Si el DataFrame está vacío, se muestra un mensaje de error.
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
    Función principal del programa que se encarga de la codificación del texto a partir de Pi.

    Esta función se encarga de leer el archivo de texto a codificar, crear una instancia de PiEncoder, 
    buscar el mapeo óptimo y generar/imprimir el dataframe correspondiente.

    Args:
        archivo (str): Ruta al archivo con el texto a codificar.
        start (int, opcional): Índice de inicio del texto a codificar. Por defecto es 0.
        end (int, opcional): Índice de fin del texto a codificar. Por defecto es 0.
        n (int, opcional): Número de decimales de Pi a utilizar. Si no se especifica, se calcula automáticamente.
        archivo_precomp (str, opcional): Ruta al archivo con los decimales de Pi precomputados. 
        Si no se especifica, se generan los decimales necesarios.
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

    #
    # Creamos una instancia de PiEncoder con el texto del Quijote
    mapper = PiEncoder(file_data, n, archivo_precomp)

    print("Buscando el mapeo válido...")
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
    """
    Bloque que permite ejecutar el script de forma independiente.

    Este bloque define la interfaz de línea de comandos del script y llama a la función principal `main`.
    Los argumentos requeridos y opcionales se definen mediante `argparse.ArgumentParser`.
    """
    parser = argparse.ArgumentParser(description="Interfaz de línea de comandos de PiEncoder")
    parser.add_argument("nombre_archivo", help="Ruta al archivo de texto de entrada")
    parser.add_argument("-s", "--inicio", type=int, default=0, help="Número de lineas para saltar desde el principio del archivo")
    parser.add_argument("-e", "--final", type=int, default=0, help="Número de lineas para saltar desde el final del archivo")
    parser.add_argument("-n", "--establecer-n", type=int, default=None, help="Establecer un valor explícito para n")
    parser.add_argument("-p", "--archivo-pi", type=str, default=None, help="Ruta a un archivo con decimales precalculados de Pi")
    argumentos = parser.parse_args()
    main(argumentos.nombre_archivo, argumentos.inicio, argumentos.final, argumentos.establecer_n, argumentos.archivo_pi)
