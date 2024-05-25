import pandas as pd
import os

# Obtener la ruta del archivo Excel
carpeta = 'bd_aerolineas'
archivo_excel = os.path.join(carpeta, 'BD_Trafico_aereo-2014-2024-1.xls')

# Cargar el archivo Excel en un DataFrame
df = pd.read_excel(archivo_excel)

# Filtrar las filas con valor 0 en la columna 'PASAJEROS'
df_filtrado = df[df['PASAJEROS'] != 0]

# Eliminar las columnas desde 'ORIG_2_N' hasta 'OPER_2'
columnas_a_eliminar = df.columns[df.columns.get_loc('ORIG_2_N'):df.columns.get_loc('OPER_2')+1]
df_filtrado = df_filtrado.drop(columns=columnas_a_eliminar)

# Guardar el DataFrame filtrado en un nuevo archivo Excel con extensión .xlsx
archivo_salida = os.path.join(carpeta, 'BD_Trafico_aereo_filtrado.xlsx')
df_filtrado.to_excel(archivo_salida, index=False)
