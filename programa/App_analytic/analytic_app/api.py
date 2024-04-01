import requests
from django.conf import settings

def obtener_datos():
    response = requests.get(f"{settings.API_BASE_URL}/db_get_row.php")
    if response.status_code == 200:
        return response.json()
    else:
        print("Error al recuperar los datos")
        return None
    
def enviar_datos(data):
    response = requests.post(f"{settings.API_BASE_URL}/db_insert_row.php", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error al enviar los datos")
        return None