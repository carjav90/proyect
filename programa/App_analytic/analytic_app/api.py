from django.http import JsonResponse
import json
import requests
from django.conf import settings


def obtener_datos():
    data = {
    "szName": "Test",
    "dbName": "dbtest",
    "szTable": "tbMovs",
    "szFields": "szConcept, dDate, fValue, acType",
    # "szWhere": "WHERE acType = '0000'" # Opcion para filtrar por el acType de cada registro
}
    response = requests.post(f"{settings.API_BASE_URL}/db_get_rows.php", json=data)
    print("Respuesta de la API:", response.text)
    if response.status_code == 200:
        try:
            result = response.json()
            return result["Description"]
        except json.JSONDecodeError as e:
            print("Error decodificando JSON:", e)
            return {"error": "Error descodifiacion JSON"}

    else:
        print("Error al recuperar los datos", response.status_code)
        return {"error": f"Error e la respuesta de la API: {response.status.code}"}
    
    data2 = {

    }


def enviar_datos(data):
    response = requests.post(f"{settings.API_BASE_URL}/db_insert_row.php", json=data)
    if response.status_code == 200:
        print("Datos enviados correctamente")
        return JsonResponse(response.json())
    
    else:
        print("Error al enviar los datos")
        return JsonResponse({'error': 'Error al enviar los datos'}, status = response.status_code)