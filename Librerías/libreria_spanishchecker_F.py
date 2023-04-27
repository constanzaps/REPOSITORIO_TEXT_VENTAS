
"""
Created on Sat Apr 15 21:27:12 2023

@author: Coni

spanishchecker ya no está disponible.

"""


!pip install spanishchecker

import spanishchecker
import pandas as pd
import os

#Definimos variables
path= '/Users/Coni/Desktop/Proyectos/data_preprocessing.xlsx'
col_txt = 'texto0' #Nombre de columna que se quiera analizar


df = pd.read_excel(path)

def chequear(text):
    
    # Create a SpanishChecker object
    checker = spanishchecker.SpanishChecker()

    # Get the number of orthographic errors
    num_errors = checker.count_errors(text)
    return num_errors

df['num_errors_SpanCh'] = df[col_txt].apply(lambda x: chequear(x))


df['errores_porc_SpanCh'] = df['num_errors_SpanCh']/ data['cant_palabras'] 

#Guardamos archivo
dir_path, filename1 = os.path.split(path)
filename, extension = os.path.splitext(filename1)
path_result= dir_path + '/' +filename+ '__result_SpanCh.xlsx'


df.to_excel(path_result)