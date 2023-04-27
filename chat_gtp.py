#Importamos librerías y leemos archivo
#!pip install openai
import os
import pandas as pd
import datetime
import openai
import re

#Definimos variables
path= '/Users/Coni/Desktop/Proyectos/data_preprocessing.xlsx'
columnas = {'id': int, 'user_id': int, 'texto0': str}
col_txt = 'texto0' #Nombre de columna que se quiera analizar



data = pd.read_excel(path)
data= data.head(10)

openai.api_key = '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'

def count_spelling_mistakes(text):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Cuenta el número de errores ortográficos en el siguiente texto:\n{text}\n\nEl número de errores ortográficos es:",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    result = response.choices[0].text.strip()
    result_sin_puntos = result.replace(".", "")

    return int(result_sin_puntos)


# Aplica la función a la columna 'texto'
data['cant_errores_openai'] = data[col_txt].apply(count_spelling_mistakes)

#Guardamos archivo
dir_path, filename1 = os.path.split(path)
filename, extension = os.path.splitext(filename1)
path_result= dir_path + '/' +filename+ '__openai2.xlsx'


data.to_excel(path_result)

now = datetime.datetime.now()
print("End time: ", now)