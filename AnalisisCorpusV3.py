# %%
# Todos los imports van al principio
import pandas as pd
import warnings
import time
import itertools
from textwrap import wrap
import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path

# %pip install wget
# !python -m wget  https://www.gutenberg.org/cache/epub/2000/pg2000.txt

# %%
# Función para configurar la visualización de los gráficos
def setup_plots():
    plt.rcParams["figure.figsize"] = (20,10)
    plt.rcParams["figure.dpi"] = 300
    plt.rcParams["savefig.dpi"] = 300
    plt.rcParams["savefig.bbox"] = 'tight'
    plt.rcParams["savefig.pad_inches"] = 0.1
    plt.rcParams["savefig.transparent"] = True
    plt.rcParams["savefig.format"] = 'png'
    plt.rcParams["savefig.facecolor"] = 'white'
    plt.rcParams["savefig.edgecolor"] = 'white'
    plt.rcParams["savefig.orientation"] = 'landscape'

# Función para generar una lista de caracteres únicos
def get_unique_chars(text, step):
    charset_list = []
    for i in range(0, len(text), step):
        charset_list.append(len(set(text[:i])))
    return charset_list

# Función para crear un DataFrame de los caracteres únicos
def create_df(charset_list, total_chars):
    df = pd.DataFrame(
        {
            'Posición': range(0, len(charset_list)),
            'Caracteres únicos': charset_list,
            'Porcentaje de caracteres únicos': [(x/total_chars)*100 for x in charset_list]
        }
    )
    return df.style.format({'Porcentaje de caracteres únicos': '{:,.2f}%'.format}).hide_index()

# Función para graficar los caracteres únicos
def plot_unique_chars(charset_list, title, xlabel, ylabel, xticks=None, yticks=range(0, 100, 5), log_scale=False):
    setup_plots()
    plt.grid()
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if xticks:
        plt.xticks(xticks)
    plt.yticks(yticks)
    plt.plot(charset_list)
    if log_scale:
        plt.yscale('log')
    plt.show()

# Función para imprimir caracteres únicos
def print_unique_chars(text):
    unique_chars = "".join(sorted(set(text)))
    print(unique_chars, len(unique_chars))

# Función para obtener y ordenar la cuenta de caracteres
def get_sorted_char_count(text):
    char_count = Counter(text)
    return sorted(char_count.items(), key=lambda x: x[1], reverse=True)

# Función para graficar la distribución de caracteres
def plot_char_distribution(sorted_char_count, log_scale=False):
    total_chars = len(sorted_char_count)
    plt.bar(range(total_chars), [x[1] for x in sorted_char_count], align='center')
    plt.xticks(range(total_chars), [x[0] for x in sorted_char_count])
    if log_scale:
        plt.yscale('log')
    plt.show()

# Función para imprimir caracteres en orden de frecuencia
def print_chars_by_frequency(sorted_char_count):
    print("".join([x[0] for x in sorted_char_count]))


# Configuración
warnings.simplefilter(action='ignore', category=FutureWarning)

# Cargar datos
recursos = Path.cwd() / "recursos"
quijote_file = recursos / 'pg2000.txt'

with open(quijote_file, 'r', encoding='utf-8-sig') as file:
    quijote_data = ''.join(file.readlines()[36:-372])

# Características básicas del texto
unique_chars = len(set(quijote_data))
text_length = len(quijote_data)

print("Número de caracteres únicos: ", unique_chars)
print("Longitud en caracteres del texto: ", text_length)

# Contar caracteres únicos
charset_list_1 = get_unique_chars(quijote_data, 1)
df = create_df(charset_list_1, unique_chars)
df

# Graficar caracteres únicos
plot_unique_chars(charset_list_1, 'Caracteres únicos', 'número de ronda', 'caracteres únicos')

# Repetir el proceso para cada 1000 caracteres
charset_list_1000 = get_unique_chars(quijote_data, 1000)
df = create_df(charset_list_1000, unique_chars)
df

plot_unique_chars(charset_list_1000, 'Caracteres únicos cada 1000 caracteres', 'número de ronda (*1000 caracteres)', 'caracteres únicos', xticks=range(0, 2100, 100))

# Imprimir caracteres únicos
print_unique_chars(quijote_data)

# Analizar la distribución de los caracteres en el texto
sorted_char_count = get_sorted_char_count(quijote_data)

# Mostrar la distribución de los caracteres en el texto
plot_char_distribution(sorted_char_count)
plot_char_distribution(sorted_char_count, log_scale=True)

# Imprimir los caracteres en orden de frecuencia
print_chars_by_frequency(sorted_char_count)
