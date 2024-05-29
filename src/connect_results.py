import pandas as pd
import os
import random


folder_1 = './db_Final'
folder_2 = './resultado_analisis'
archivo_excel_1 = os.path.join(folder_1, 'BD_Trafico_aereo_filtrado.xlsx')
archivo_excel_2 = os.path.join(folder_2, 'bd_resultados.xlsx')
delete_colums = {"Cod_Operador", "Grupo", "ORIG_1", "DEST_1", "Año", "ORIG_1_PAIS", "DEST_1_PAIS", "PAX_LIB", "ORIG_2", "DEST_2", "NAC", "CAR_LIB", "Distancia"}
Months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
Promedios = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


df = pd.read_excel(archivo_excel_1)
df.rename(columns={'ORIG_1_N': 'ORIGEN', 'DEST_1_N': 'DESTINO'}, inplace=True)

df_resultados = pd.read_excel(archivo_excel_2)


peso_kg_total = df_resultados["PESO_KG"].sum()
peso_kg_extra_total = peso_kg_total + df_resultados["PESO_KG_EXTRA"].sum()

df["Mes"] = df["Mes"].astype(str).replace({
    '1': 'Enero',
    '2': 'Febrero',
    '3': 'Marzo',
    '4': 'Abril',
    '5': 'Mayo',
    '6': 'Junio',
    '7': 'Julio',
    '8': 'Agosto',
    '9': 'Septiembre',
    '10': 'Octubre',
    '11': 'Noviembre',
    '12': 'Diciembre'
})


for i in range (12):
    mes = Months[i]
    df_months = df[df["Mes"] == mes]
    suma_mes = int(((df_months["CARGA (Ton)"]*1000).mean())/2)
    suma_pasj = int((((df_months["PASAJEROS"])/(28 if(i==2) else (31 if(i%2 == 0) else 30))).mean())/2)
    Promedios[i] = suma_mes
    prom = 0


df["Exceso_peso_kg"] = False
df["Exceso_peso_extra_kg"] = False


for i in range(12):
    mes = Months[i]
    promedio_mes = Promedios[i]

    df_mes = df[df["Mes"] == mes].copy()

    for index, row in df_mes.iterrows():
        carga_ajustada = (row["CARGA (Ton)"] * 1000) / 31 / 2 
        promedio_ajustado = promedio_mes - carga_ajustada
        num_pasj = len(df_resultados)
        promedio_ajustado = (num_pasj*promedio_ajustado)/(random.randint(14, 20)*14)

        df.loc[index, "Exceso_peso_kg"] = peso_kg_total > promedio_ajustado
        df.loc[index, "Exceso_peso_extra_kg"] = peso_kg_extra_total > promedio_ajustado


df_filtrado = df.drop(columns=delete_colums)
archivo_salida_final = os.path.join(folder_1, 'db_Final.xlsx')
df_filtrado.to_excel(archivo_salida_final, index=False)