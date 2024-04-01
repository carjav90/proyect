from django.http import JsonResponse
from .models import FileJSON
import json
from django.shortcuts import render

# Importacion de las funciones de API
from .api import obtener_datos, enviar_datos

def mi_vista(request):
    datos = obtener_datos()

    return render(request, "plantilla.html", {"datos":datos})




