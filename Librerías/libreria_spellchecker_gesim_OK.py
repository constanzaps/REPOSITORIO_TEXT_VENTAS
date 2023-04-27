
"""
@author: Coni


Se instancia un objeto SpellChecker con el idioma español y se crea un 
diccionario de palabras a partir de los textos.

Se agregan dos nuevas columnas al archivo de Excel: num_errors_SC que 
contiene el número de errores ortográficos encontrados en cada texto y 
errores_porc_SC que representa el porcentaje de palabras con errores 
ortográficos en cada texto.

Gensim se utiliza para crear un diccionario de palabras a partir del 
texto y para calcular la riqueza lexicográfica.


"""



!pip install pyspellchecker
import pandas as pd
from spellchecker import SpellChecker
from gensim.utils import tokenize
from gensim.corpora.dictionary import Dictionary
import os

#Definimos variables
path= '/Users/Coni/Desktop/Proyectos/data_preprocessing__openai2__result_LT.xlsx'
col_txt = 'texto0' #Nombre de columna que se quiera analizar


df = pd.read_excel(path)
# crear una instancia de SpellChecker
spell = SpellChecker(language='es')

# crear el diccionario de palabras a partir del texto
docs = [list(tokenize(text, lowercase=True)) for text in df[col_txt]]
dictionary = Dictionary(docs)

# agregar una nueva columna con el número de errores ortográficos
df['num_errors_SC'] = df[col_txt].apply(lambda x: len(spell.unknown(x.split())))


df['errores_porc_SC'] = df['num_errors_SC']/ df['cant_palabras'] 


# agregar una nueva columna con la riqueza lexicográfica
df['vocab_richness_SCyG'] = df[col_txt].apply(lambda x: len(set(list(tokenize(x, lowercase=True)))) / len(list(tokenize(x, lowercase=True))))

#Guardamos archivo
dir_path, filename1 = os.path.split(path)
filename, extension = os.path.splitext(filename1)
path_result= dir_path + '/' +filename+ '__result_SCyG.xlsx'


df.to_excel(path_result)