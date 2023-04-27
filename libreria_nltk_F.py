"""
Created on Sat Apr 15 21:27:12 2023

@author: Coni

La idea es usar enchart y nltk.

Fallo: Enchart no tiene dic en español disponible. Solo obtendremos abundancia lexicográfica de nltk.

"""
#!pip install pyenchant
!pip install pyenchant[es]
import pandas as pd
import enchant
import os
import nltk
from nltk.tokenize import word_tokenize


#Definimos variables
path= '/Users/Coni/Desktop/Proyectos/data_preprocessing.xlsx'
col_txt = 'texto0' #Nombre de columna que se quiera analizar


df = pd.read_excel(path)

# Creamos un diccionario en español
d = enchant.Dict("es")


def faltas_ort(text):
    # Tokenizamos el texto
    tokens = word_tokenize(text)
    
    # Contamos las palabras con faltas ortográficas
    num_misspelled_words = sum([not d.check(token) for token in tokens])
    return num_misspelled_words

df['num_errors_NLTK'] = df[col_txt].apply(lambda x: faltas_ort(x))


df['errores_porc_NLTK'] = df['num_errors_NLTK']/ data['cant_palabras'] 

#Guardamos archivo
dir_path, filename1 = os.path.split(path)
filename, extension = os.path.splitext(filename1)
path_result= dir_path + '/' +filename+ '__result_NLTK.xlsx'


df.to_excel(path_result)