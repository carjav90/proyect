from django.http import JsonResponse
from .models import FileJSON
import json

# Cargar aarchivo Json

# def update_json(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             file_new = FileJSON(archivo = data)
#             file_new.save()
#             return JsonResponse({"mensaje": "Archivo cargado con exito"}, status = 201)
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Formato Json inválido"}, status = 400)
#     return JsonResponse({"error": "Método no permitido"}, status = 405)



