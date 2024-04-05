from django.http import JsonResponse
import json
from io import StringIO
from datetime import datetime
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Debe ser llamado antes de importar plt
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Importacion de las funciones de API
from .api import obtener_datos, enviar_datos, enviar_datos_json

# Importar funciones de nuestro archivo de funciones de análisis
from .data_analysis_functions import Analyzer

#==================================================================================================
#==================================== OBTENER Y PROCESAR DATOS ====================================
#==================================================================================================
# def obtener_y_procesar_datos(id_user, acType):
#     # Datos a solicitar a la DB
#     data = {
#         "szName": "DataInsert",
#         "dbName": "dbaibf",
#         "szTable": "tbDataInsert",
#         "szFields": "id, id_user, dInsertDate, dDate, szConcept, fValue, acType",
#         "szWhere": f"WHERE id_user = {id_user} and acType = {acType}" # Opcion para filtrar por el acType de cada registro
#     }

#     # Solicita los datos a api.py de nuestra Api con los parametros de data
#     datos = obtener_datos(data)

#     # Solicita a la Clase Analyzer informacion mediente su metodo .conv_json_df
#     # y almacena el resultado en un diccionario llamado context
#     analyzer = Analyzer() 
#     context = analyzer.conv_json_df(datos)
#     # Tipo de acType
#     if acType == "0001":
#         dato = "Ingresos"    
#     else:
#         dato = "Gastos"
#     return context


#==================================================================================================
#=========================== DATOS A MOSTRAR EN PLANTILLA.HTML ====================================
#==================================================================================================
@csrf_exempt
def reporte(request, id_user=None, acType=None, as_view=True):
    if request.method == 'POST' or (id_user and acType):
        id_user = id_user or request.POST.get('id_user')
        acType = acType or request.POST.get('acType')

    if not id_user or not acType:
        # Si falta alguna información, manejar el error o devolver una página diferente
        return render(request, "plantilla.html")
        
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

    # Solicita los datos a api.py de nuestra Api con los parametros de data
    datos = obtener_datos(data)

    # Solicita a la Clase Analyzer informacion mediente su metodo .conv_json_df
    # y almacena el resultado en un diccionario llamado context
    analyzer = Analyzer() 
    context = analyzer.conv_json_df(datos)
    # Crea una clave dato dentro del diccionario context con el valor de dato anterior 
    context["Dato"] = dato 
    print(analyzer.conv_concept()) # Visualizacion por terminal

    # Pivotar conceptos en columnas
    result_df = analyzer.conv_concept()
    data = result_df.reset_index().values.tolist() # Convierte las filas en listas y los almacene en data
    columns = result_df.reset_index().columns.tolist() # Convierte los nombres de la columnas en una lista llamada columns
    # Agregar al context las listas de data y columns
    context.update({"data": data, "columns":columns})

    # Convertir conceptos en columnas y sumarlos por conceptos
    result_for_concept = analyzer.expenses_for_concept()

    # Mostrar cada concepto del diccionario con su valor
    print(result_for_concept)

    #Separa clave y valor en 2 listas para poder pasarlo a context
    claves = []
    valores = []
    for clave, valor in result_for_concept.items():
        print(f"Concepto: {clave}, Importe Total: {valor}")
        claves.append(clave)
        valores.append(valor)
    
    context.update({"Conceptos": claves, "Importes":valores})


    # Extraer el periodo de análisis de los datos
    periodo_min, periodo_max = analyzer.periodo()
    context.update({"Periodo_min": periodo_min, "Periodo_max":periodo_max})
    print(f"Periodo comprendido entre {periodo_min} y {periodo_max}")


    result_months = analyzer.expenses_for_months()
    context.update({"result_months": result_months})

    if as_view:
        return render(request, "plantilla.html", context) # Devuelve un http response
    else:
        return context  # Devuelve solo el contexto para ser utilizado por otra función

#==================================================================================================
#============================= DATOS A MOSTRAR EN ENVIAR.HTML =====================================
#==================================================================================================

# 3 Insertar los datos en la DBaibf en la tbDataInsert
# Envio de datos uno a uno, insertando los datos en la pagina /enviar, en la plantilla enviar.html
# y enviandolo a api.py para que los envie a nuestra base de datoS

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

#==================================================================================================
#============================= DATOS A MOSTRAR EN ENVIAR2.HTML ====================================
#==================================================================================================

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
    

#==================================================================================================
#============================= DATOS A MOSTRAR EN TIME_SERIES.HTML ================================
#==================================================================================================

def time_series(request):

    context = {}

    if request.method == 'POST':
        id_user = request.POST.get('id_user')
        acType = request.POST.get('acType')

        if id_user and acType:
            # Llama a reporte para obtener los datos
            datos = reporte(request, id_user=id_user, acType=acType, as_view=False)
            
            if 'result_months' in datos:
                result_months = datos['result_months']
                
                # Aquí generarías la gráfica con los datos de result_months
                # Suponiendo que result_months es un DataFrame con una columna 'Total' y el índice como 'Mes'
                
                fig, ax = plt.subplots(figsize=(8, 4))
                result_months.plot(ax=ax)  # Asumiendo que el índice es la fecha
                ax.set_title('Total Mensual')
                ax.set_xlabel('Mes')
                ax.set_ylabel('Total')

                # Guardar gráfica en un buffer en formato PNG
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                plt.close(fig)  # No olvides cerrar la figura para liberar memoria
                buffer.seek(0)
                image_png = buffer.getvalue()
                buffer.close()

                # Convertir buffer a cadena base64 y decodificar
                graphic = base64.b64encode(image_png).decode('utf-8')
                context['graphic'] = graphic
            else:
                context['error'] = 'Datos no disponibles para generar la gráfica.'
        else:
            context['error'] = 'ID de usuario o tipo de acción faltantes.'
    return render(request, 'time_series.html', context)

