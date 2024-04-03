from django.http import JsonResponse
import json
from io import StringIO
from datetime import datetime
import pandas as pd
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Importacion de las funciones de API
from .api import obtener_datos, enviar_datos, enviar_datos_json

@csrf_exempt
def reporte(request):
    if request.method == 'POST':
        id_user = request.POST.get('id_user')
        acType = request.POST.get('acType')

        data = {
            "szName": "DataInsert",
            "dbName": "dbaibf",
            "szTable": "tbDataInsert",
            "szFields": "id, id_user, dInsertDate, dDate, szConcept, fValue, acType",
            "szWhere": f"WHERE id_user = {id_user} and acType = {acType}" # Opcion para filtrar por el acType de cada registro
        }  
        datos = obtener_datos(data) 

        if acType == "0001":
            dato = "Ingresos"    
        else:
            dato = "Gastos"

        if 'error' in datos:
            context = {"error": datos["error"]}
        else:
            # Formatear las fechas antes de pasar los datos a la plantilla
            for desc in datos:

                # Convierte los datos de las ferchas a Strings para que se puedan introducir en el JSON con el resto de datos           
                # Para 'dDate'
                if isinstance(desc['dDate'], dict) and 'date' in desc['dDate']:
                    fecha_str = desc['dDate']['date']
                    fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S.%f')
                    desc['dDate'] = fecha_obj.strftime('%Y-%m-%d')  # Formato simplificado para 'dDate'
                
                # Para 'dInsertDate'
                if isinstance(desc['dInsertDate'], dict) and 'date' in desc['dInsertDate']:
                    fecha_insert_str = desc['dInsertDate']['date']
                    fecha_insert_obj = datetime.strptime(fecha_insert_str, '%Y-%m-%d %H:%M:%S.%f')
                    desc['dInsertDate'] = fecha_insert_obj.strftime('%Y-%m-%d')  # Formato simplificado para 'dInsertDate'
            
            # Serializacion de los datos en JSON
            datos_json = json.dumps(datos)
            datos_json_io = StringIO(datos_json)
            df = pd.read_json(datos_json_io, dtype={'acType': 'str'})
            print(df)
            # Convertir las fechas a formato datetime, si no lo están
            df['dDate'] = pd.to_datetime(df['dDate'])
            df['dInsertDate'] = pd.to_datetime(df['dInsertDate'])

            # Asegúrate de que las fechas estén en el formato correcto
            df['dDate'] = df['dDate'].dt.strftime('%Y-%m-%d')
            df['dInsertDate'] = df['dInsertDate'].dt.strftime('%Y-%m-%d')
            df.sort_values(by="dDate", inplace = True)# Ordenar por la columna dDate
            datos_ordenados = df.to_dict('records')

            df.set_index("dDate", inplace=True)
            # df = df.drop(columns='dDate')
            df.sort_values(by="dDate", inplace = True)# Ordenar por la columna dDate
            # datos_ordenados = df.to_dict("records")

            # Suma de la columna fValue y redondeo de a 2 decimales
            suma = round(df['fValue'].sum(), 2)
            print(df)

            # Contar nº de registros
            count = df["szConcept"].count()
            context = {"Description": datos_ordenados,
                        "Resultado_Suma": suma,
                        "n_de_registros": count,
                        "Dato": dato}
            # print("El valor de la suma de fValue es:", suma)
    else:
        return render(request, "plantilla.html")
    return render(request, "plantilla.html", context)

# 3 Insertar los datos en la DBaibf en la tbDataInsert
# Envio de datos uno a uno, insertando los datos en la pagina /enviar, en la plantilla enviar.html
# y enviandolo a api.py para que los envie a nuestra base de datos y 

def envio_datos(request):
    if request.method == 'POST':
        id_user = request.POST.get('id_user')
        dInsertDate = request.POST.get('dInsertDate')
        dDate = request.POST.get('dDate')
        szConcept = request.POST.get('szConcept')
        fValue = request.POST.get('fValue')
        acType = request.POST.get('acType')
        data = {
            "szName": "dbDataInsert JSON",
            "szDbName": "dbaibf",
            "szTable": "tbDataInsert",
            "szFields": "id_user, dInsertDate, dDate, szConcept, fValue, acType",
            "szValues": f"{id_user}, '{dInsertDate}', '{dDate}', '{szConcept}', {fValue}, '{acType}'"
        }
        # Llamar a la función enviar_datos para enviar 'data' a la API
        return enviar_datos(data)
    else:
        # Mostrar el formulario para insertar los datos de un registro
        return render(request, "plantilla_enviar.html")


# Envio de datos desde un archivo json, insertando el archivo en la pagina /enviar2, en la plantilla enviar_json.html   
# LEEE ARCHIVO JSON Y LO VA ENVIANDO UNO A UNO A LA API
 
def envio_json(request):
    if request.method == 'POST' and request.FILES.get('json_file'):
        # Procesar el archivo JSON subido
        json_file = request.FILES['json_file']
        data_json = json.load(json_file)
        lk_values = data_json.get('lkValues', [])

        responses = []
        for valores in lk_values:
            data = {
                "szName": "dbDataInsert JSON",
                "szDbName": "dbaibf",
                "szTable": "tbDataInsert",
                "szFields": "id_user, dInsertDate, dDate, szConcept, fValue, acType",
                "szValues": f"{valores[0]}, '{valores[1]}', '{valores[2]}', '{valores[3]}', {valores[4]}, '{valores[5]}'"
            }

            # Llamar a la función enviar_datos_json para enviar 'data' a la API
            response = enviar_datos_json(data)
            responses.append(response)
        return JsonResponse({'status': 'success', 'responses': responses})

    elif request.method == 'GET':
        # Mostrar el formulario para subir el archivo
        return render(request, 'plantilla_enviar_json.html')
