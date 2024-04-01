import json
import requests
from django.conf import settings
import _json

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
    data = {
    "szName": "dbtest JSON",
    "dbName": "dbaibf",
    "szTable": "tbDataInsert",
    "szFields": "id, id_user, dInsertDate, dDate, szConcept, fValue, acType",
    "jsValues": [
        {
            "id": 1,
            "id_user": 1,
            "dInsertDate": "08-04-2024",
            "dDate": "08-04-2024",
            "szConcept": "POSTMAN BORJa",
            "fValue": 1025.50,
            "acType": "0000"
        }
    ]
}
    response = requests.post(f"{settings.API_BASE_URL}/db_insert_row.php", json=data)
    if response.status_code == 200:
        print("Datos enviados correctamente")
        return response.json()
    
    else:
        print("Error al enviar los datos")
        return None