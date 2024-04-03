from django.http import JsonResponse
import json
from io import StringIO
from datetime import datetime
import pandas as pd
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Importacion de las funciones de API
from .api import obtener_datos, enviar_datos, enviar_datos_json

# Importar funciones de nuestro archivo de funciones de análisis
from .data_analysis_functions import conv_json_df, conv_concept

@csrf_exempt
def reporte(request):
    if request.method == 'POST':
        id_user = request.POST.get('id_user')
        acType = request.POST.get('acType')
        
        # Tipo de acType
        if acType == "0001":
            dato = "Ingresos"    
        else:
            dato = "Gastos"

        # Datos a solicitar a la DB
        data = {
            "szName": "DataInsert",
            "dbName": "dbaibf",
            "szTable": "tbDataInsert",
            "szFields": "id, id_user, dInsertDate, dDate, szConcept, fValue, acType",
            "szWhere": f"WHERE id_user = {id_user} and acType = {acType}" # Opcion para filtrar por el acType de cada registro
        }  
        datos = obtener_datos(data) 
        context = conv_json_df(datos)
        context["Dato"] = dato
              

        
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
