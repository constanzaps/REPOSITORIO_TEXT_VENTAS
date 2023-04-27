#Importamos librerías y leemos archivo
import pandas as pd
import re
import nltk
import string
nltk.download('stopwords')
import chardet
#Corregimos codificación
#!pip install ftfy
import ftfy
import os
import datetime

#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


#Ejemplo de error linea 153 CSV

#Definimos variables
path= '/Users/Coni/Desktop/Proyectos/audios.csv'
columnas = {'id': int, 'user_id': int, 'texto0': str}
col_txt = 'texto0' #Nombre de columna que se quiera analizar
eliminar_users ='user_id'
eliminar_rango=range(1, 15)
dir_path, filename = os.path.split(path)


def abrir_archivo(path):
    """
    Esta función recibe la ruta del archivo y lo abre.
    ej. path = '/Users/Coni/Desktop/Proyectos/audios.csv'
    """
    # Detectar la codificación del archivo
    with open(path, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']
    print(encoding)
    # Leer el archivo con la codificación detectada
    data = pd.read_csv(path, encoding=encoding)
    return data

data=abrir_archivo(path)


def preprocesamiento(columnas,col_txt,data,eliminar_users='',eliminar_rango=''):
    """
    Del dataset extraemos solo columnas relevantes para el análisis.
    Se realiza el siguiente procesamiento:
    1. Eliminar filas con NaN en comentarios -> No tiene sentido realizar NLP - Me avisan si prefieren dejarlas
    2. Cambiar el tipo de datos de las columnas del DataFrame
    3. Quitamos usuarios que se usaron como prueba para ingreso en formulario [1,14]
    4. Mostramos y eliminamos problemas de codificación. 
    5. Finalmente quitamos elementos irrelevantes para el análisis, que son:
        -  Eliminamos las puntuaciones 
        - Eliminamos los espacios extra
        - Quitar numeros
    6. Añadimos columna que nos cuente la cantidad de palabras por comentario
    NOTA: ERROR DE CODIFICACIÓN: Vemos que la cadena original estaba codificada en latin1, 
    pero se interpretó como utf-8. Lo cual implica problemas con las tildes en las oraciones.
    """
    names_col= list(columnas.keys())
    data=data[names_col]
    #1.
    data = data.dropna(subset=[col_txt])     
    data = data.dropna(subset=[col_txt]) #Quitamos los NaN
    data[col_txt] = data[col_txt].fillna('') #Quitamos los NaN
    
    #2.
    data = data.astype(columnas)
    #3.
    if eliminar_users != '':
        data = data[~data[eliminar_users].isin(eliminar_rango)] 

    #4.
    #Vemos que existen problemas con ciertas líneas, por temas de codificación 
    print('\t Vemos fallas de codificación:')
    print(data.iloc[842,2] ) #problema tilde
    print(data.iloc[843,2]) #problema tilde
    print(data.iloc[27,2]) #problema ñ
    
    data[col_txt] = data[col_txt].apply(ftfy.fix_text)


    data[col_txt] = data[col_txt].astype(str) #Quitamos los NaN

    #5.
    regex = re.compile('[%s]' % re.escape(string.punctuation + '¿¡'))
    data[col_txt] = data[col_txt].apply(lambda x: regex.sub('', x) if x is not None else x)
    data[col_txt] = data[col_txt].apply(lambda x: ' '.join(x.split()) if x is not None else x)
    data[col_txt] = data[col_txt].apply(lambda x: ' '.join([s for s in x.split() if not any(c.isdigit() for c in s)]) if x is not None else x)
  
    
    #4.
    #Vemos que existen problemas con ciertas líneas, por temas de codificación 
    print('\t Corrección de fallas de codificación:')
    print(data.iloc[842,2] ) #problema tilde
    print(data.iloc[843,2]) #problema tilde
    print(data.iloc[27,2]) #problema ñ
    
    #6.
    data['cant_palabras'] = data[col_txt].apply(lambda x: len(x.split()))

    return data


data= preprocesamiento(columnas,col_txt,data,eliminar_users,eliminar_rango)

#Guardamos archivo
dir_path, filename = os.path.split(path)
now = datetime.datetime.now()
time_str = now.strftime("%d%m%Y%H%M")

path_result= dir_path + '/' + 'data_preprocessing.xlsx'

data.to_excel(path_result)

