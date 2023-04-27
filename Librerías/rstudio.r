# install.packages("openxlsx")
# install.packages("hunspell")
# install.packages("quanteda")
# install.packages("quanteda.textstats")
# install.packages("quanteda.type_token_ratio")

# "TTR":
#   The ordinary Type-Token Ratio:
#   
#   TTR = \frac{V}{N}
#   


library(openxlsx)
library(quanteda)
library(quanteda.textstats)

#Seteamos parámetros
path <- 'C:\\Users\\Coni\\Desktop\\Proyectos\\data_preprocessing__result_SCyG__result_LT.xlsx'
col_txt <- 'texto0' #Nombre de columna que se quiera analizar

#Seteamos parámetros
path <- 'C:\\Users\\Coni\\Desktop\\Proyectos\\data_preprocessing__result_SCyG__result_LT.xlsx'
col_txt <- 'nota_0' #Nombre de columna que se quiera analizar




datos <- read.xlsx(path)


texto <- datos$`texto0`

# Convertir la columna en una cadena de texto
datos[[col_txt]] <- as.character(datos[[col_txt]])


#Tokenizamos palabras
palabras <- tokens(texto, remove_punct = TRUE, remove_numbers = TRUE, remove_symbols = TRUE)

# Convertir el objeto de tokens a un objeto dfm
dfm_palabras <- dfm(palabras)

# Crear columna con cantidad de errores

# Calcular la riqueza de vocabulario
diversidad_lexica <- textstat_lexdiv(dfm_palabras, "TTR")
# Unir resultados al dataframe original
datos$diversidad_lexica_TTR <- diversidad_lexica$TTR

# Calcular la riqueza de vocabulario
diversidad_lexica <- textstat_lexdiv(dfm_palabras, "C")
# Unir resultados al dataframe original
datos$diversidad_lexica_C <- diversidad_lexica$C

# Calcular la riqueza de vocabulario
diversidad_lexica <- textstat_lexdiv(dfm_palabras, "R")
# Unir resultados al dataframe original
datos$diversidad_lexica_R <- diversidad_lexica$R

# Calcular la riqueza de vocabulario
diversidad_lexica <- textstat_lexdiv(dfm_palabras, "CTTR")
# Unir resultados al dataframe original
datos$diversidad_lexica_CTTR <- diversidad_lexica$CTTR


# Guardar los resultados en un archivo Excel
write.xlsx(datos, "C:\\Users\\Coni\\Desktop\\Proyectos\\data_preprocessing__result_SCyG__result_LT__resultR_quanteda.xlsx", colNames = TRUE)

