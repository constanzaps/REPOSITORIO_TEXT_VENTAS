import pandas as pd
    # import numpy as np
    # import re
    # import nltk
    # from nltk.tokenize import word_tokenize #Tokenizador
    # import string
    # nltk.download('stopwords')
    # from nltk.corpus import stopwords
    # from nltk.tokenize import sent_tokenize
    # from language_tool_python import LanguageTool
    # from collections import Counter
    # import chardet
    
    
path= '/Users/Coni/Desktop/Proyectos/data_preprocessing__openai2__result_LT__result_SCyG.xlsx'
columnas = {'id': int, 'user_id': int, 'texto0': str}
col_txt = 'texto0' #Nombre de columna que se quiera analizar



data = pd.read_excel(path)

errores=data[['cant_errores_openai','cant_errores_LT','num_errors_SC']]

correlation_matrix = errores.corr()
print(data.columns)


#Meta: hacer metricas dek¿l paper, ponderar, obtener promedio y clusterizar