
"""
Created on Sat Apr 15 21:27:12 2023

@author: Coni

LanguageTool es una herramienta de procesamiento de lenguaje natural que ofrece funciones
 como la corrección gramatical y ortográfica. En este caso usaremos sus herramientas de 
 corrección y explicación. Parte #1.

Para medir la abundancia léxica, LanguageTool cuenta con una métrica llamada "Richness of
 Vocabulary" o "Riqueza de Vocabulario", que proporciona una puntuación en función de la 
 diversidad léxica del texto. Se usará la métrica num_unique_words / num_words (Parte #2.) 

Dado que el código tardaba mucho incluso quitando los loop, se usará una instancia del Pool 
de procesos (Cuando se crea una instancia del objeto Pool, los procesos se distribuyen 
             en diferentes núcleos de CPU disponibles en el sistema.)

"""
#!pip install langdetect

#!pip install language-tool-python
#!pip show language-tool-python

#Importamos librerías y leemos archivo
from language_tool_python import LanguageTool
import multiprocessing as mp
import os
import pandas as pd
import winsound
import datetime

#Quitar las siguientes?
# from langdetect import detect
# from langdetect.lang_detect_exception import LangDetectException
# from collections import Counter
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords


tool = LanguageTool('es')#, disabled_categories=['UPPERCASE_SENTENCE_START'] #Desabilitamos que exija mayúsculas al comienzo





now = datetime.datetime.now()
print("Current time: ", now)


#Definimos variables
#path= '/Users/Coni/Desktop/Proyectos/data_preprocessing.xlsx'
path= '/Users/Coni/Desktop/Proyectos/data_preprocessing__openai2.xlsx'
col_txt = 'texto0' #Nombre de columna que se quiera analizar


data = pd.read_excel(path)



data[col_txt]=data[col_txt].astype(str) 

#1.

def misspelled_words(x):
    """
    Palabras que están mal escritas en un texto.
    """
    matches = tool.check(x)
    m_w = []
    for match in matches:
        if match.ruleId == 'MORFOLOGIK_RULE_ES' or match.ruleId == 'ACENTO':
            word = match.context[match.offset:match.offset+match.errorLength]
            m_w.append(word)
    return m_w

def explicacion(x):
    """
    Explicación de resultados
    """
    matches = tool.check(x)
    return matches

# Define la función que realiza la tarea para un comentario
def procesar_comentario(x):
    cant_errores = len(tool.check(x))
    palabras_erroneas = misspelled_words(x)
    explicacion_result = explicacion(x)
    return cant_errores, palabras_erroneas, explicacion_result


print('gi')

if __name__ == '__main__':
    # Llamamos a freeze_support()
    mp.freeze_support()
    
    # Crea una instancia del Pool de procesos
    pool = mp.Pool()
    print('etapa pool')

    # Paraleliza la tarea aplicando la función a cada comentario
    resultados = pool.map(procesar_comentario, data[col_txt])

    # Cierra el Pool de procesos
    pool.close()

    # Obtiene los resultados en listas separadas
    cant_errores, palabras_erroneas, explicacion_result = zip(*resultados)
    now = datetime.datetime.now()
    print("Middle time: ", now)

    # Agrega las columnas de resultados al DataFrame
    data['cant_errores_LT'] = cant_errores
    data['Palabras_erroneas_LT'] = palabras_erroneas
    data['Explicacion_LT'] = explicacion_result

    # Porcentaje de errores respecto al total
    data['errores_porc_LT'] = data['cant_errores_LT']/ data['cant_palabras'] 
    print('si se hizo 1')
    print(data.columns)


    print('etapa 2')
    #2.
    #Ahora nos dedicamos a medir la riqueza linguística
    
    now = datetime.datetime.now()
    print("Middle time after errores ortográficos: ", now)
    
    # Inicializar LanguageTool
    tool = LanguageTool('es')
    
    # Definir función para calcular la abundancia léxica de un texto
    def calculate_vocab_richness(text):
        #matches = tool.check(text) no se usa
        num_words = len(text.split())
        num_unique_words = len(set(text.split()))
        vocab_richness = num_unique_words / num_words
        return vocab_richness
    
    # Aplicar la función a la columna "texto"
    data['vocab_richness_LT'] = data[col_txt].apply(calculate_vocab_richness)
    
    print('j3j3pool')


    #Guardamos archivo
    dir_path, filename1 = os.path.split(path)
    filename, extension = os.path.splitext(filename1)
    path_result= dir_path + '/' +filename+ '__result_LT.xlsx'
    
    
    data.to_excel(path_result)
    
    now = datetime.datetime.now()
    print("End time: ", now)

