from django.http import JsonResponse
import json
from datetime import datetime
import pandas as pd
from django.shortcuts import render

# Importacion de las funciones de API
from .api import obtener_datos, enviar_datos

def mi_vista(request):
    datos = obtener_datos()
    if 'error' in datos:
        
        context = {"error": datos["error"]}
    else:
        # Formatear las fechas antes de pasar los datos a la plantilla
        for desc in datos:
            # Asegúrate de que desc['dDate']['date'] sea una cadena de fecha válida.
            fecha = datetime.strptime(desc['dDate']['date'], '%Y-%m-%d %H:%M:%S.%f')
            desc['dDate']['date'] = fecha.strftime('%Y-%m-%d')  # Formato simplificado, cambia según necesites.
        

        datos_json = json.dumps(datos)
        df = pd.read_json(datos_json)
        # Extraer la clave 'date' de cada diccionario en la columna 'dDate'
        df['date'] = df['dDate'].apply(lambda x: x['date'])
        # Convertir las fechas a formato datetime, si no lo están
        df['date'] = pd.to_datetime(df['date'])

        df.set_index("date", inplace=True)
        df = df.drop(columns='dDate')

        # Suma de la columna fValue y redondeo de a 2 decimales
        suma = round(df['fValue'].sum(), 2)
        print(df)

        # Contar nº de registros
        count = df["szConcept"].count()
        context = {"Description": datos,
                   "Resultado_Suma": suma,
                   "n_de_registros": count}
        # print("El valor de la suma de fValue es:", suma)
    return render(request, "plantilla.html", context)





