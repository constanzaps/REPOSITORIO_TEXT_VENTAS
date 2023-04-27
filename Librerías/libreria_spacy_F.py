
"""
@author: Coni


Spacy: No está optimizada para corregir el español
"""
#!pip install language-tool-python
#!pip show language-tool-python
#!pip install spacy
#!pip install spacy-es_core_news_sm
#!python -m spacy download es_core_news_sm

#Importamos librerías y leemos archivo
import pandas as pd
import spacy
import datetime



#Definimos variables
path= '/Users/Coni/Desktop/Proyectos/data_preprocessing.xlsx'
col_txt = 'texto0' #Nombre de columna que se quiera analizar

nlp = spacy.load("es_core_news_sm")
data = pd.read_excel(path)

now = datetime.datetime.now()
print("Current time: ", now)


def get_metrics(text):

    # Create a Spacy Doc object from the text
    doc = nlp(text)

    # Get the number of spelling errors in the Doc object
    num_spelling_errors = len([error for error in nlp.check_spelling(doc)])
    
    # Get the number of unique words in the Doc object
    num_unique_words = len(set(doc))

    # Return a dictionary of metrics
    return {
        "num_spelling_errors": num_spelling_errors,
        "num_unique_words": num_unique_words,
    }


data["num_spelling_errors"] = data[col_txt].apply(get_metrics).get("num_spelling_errors")
data["num_unique_words"] = data[col_txt].apply(get_metrics).get("num_unique_words")

now = datetime.datetime.now()
print("End time: ", now)