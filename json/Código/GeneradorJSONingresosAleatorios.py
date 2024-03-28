import json
import random
from datetime import datetime, timedelta
import os

def generar_ingresos(anio, ingresos_totales):
    ingresos = []

    # Ingresos mensuales
    cantidad_ingresos_mensuales = random.randint(0, ingresos_totales // 2)
    for _ in range(cantidad_ingresos_mensuales):
        ingresos.append({
            "concepto": "Subscripcion mensual",
            "fecha": f"{random.randint(1, 28)}/01/{anio}",
            "valor": 50
        })

    # Ingresos trimestrales
    cantidad_ingresos_trimestrales = random.randint(0, (ingresos_totales - len(ingresos)) // 4)
    for _ in range(cantidad_ingresos_trimestrales):
        ingresos.append({
            "concepto": "Subscripcion trimestral",
            "fecha": f"{random.randint(1, 28)}/03/{anio}",
            "valor": 120
        })

    # Ingresos semestrales
    cantidad_ingresos_semestrales = random.randint(0, (ingresos_totales - len(ingresos)) // 6)
    for _ in range(cantidad_ingresos_semestrales):
        ingresos.append({
            "concepto": "Subscripcion semestral",
            "fecha": f"{random.randint(1, 28)}/06/{anio}",
            "valor": 200
        })

    # Ingresos anuales
    cantidad_ingresos_anuales = random.randint(0, ingresos_totales - len(ingresos))
    for _ in range(cantidad_ingresos_anuales):
        ingresos.append({
            "concepto": "Subscripcion anual",
            "fecha": f"{random.randint(1, 28)}/01/{anio}",
            "valor": 350
        })

    # Ingresos diarios (artículos vendidos)
    cantidad_ingresos_diarios = ingresos_totales - len(ingresos)
    valores_articulos = {
        "articulo1": 15.25,
        "articulo2": 19.25,
        "articulo3": 45.25,
        "articulo4": 68.99,
        "articulo5": 82,
        "articulo6": 115.55,
        "articulo7": 10.05,
        "articulo8": 5.99,
        "articulo9": 71.55,
        "articulo10": 33.45,
        "articulo11": 12.25,
        "articulo12": 29.99,
        "articulo13": 19.25
    }
    numeros_articulos = list(range(1, 14))  # Considerando los primeros 13 artículos
    while cantidad_ingresos_diarios > 0:
        numero_articulo = random.choice(numeros_articulos)
        valor = valores_articulos[f"articulo{numero_articulo}"]
        ingresos.append({
            "concepto": f"Articulo {numero_articulo}",
            "fecha": f"{random.randint(1, 28)}/{random.randint(1, 12)}/{anio}",
            "valor": valor
        })
        cantidad_ingresos_diarios -= 1

    # Mezclar los ingresos
    random.shuffle(ingresos)

    return ingresos

def generar_json(ingresos):
    datos_json = {
        "szName": "expenses",
        "lszFields": [
            "szConcept",
            "dDate",
            "fValue"
        ],
        "lkValues": [[ingreso["concepto"], ingreso["fecha"], ingreso["valor"]] for ingreso in ingresos]
    }

    return datos_json

def guardar_json_en_archivo(datos_json, nombre_archivo):
    with open(nombre_archivo, 'w') as f:
        json.dump(datos_json, f, indent=4)

def main():
    anio = int(input("Ingrese el año para el periodo de ingresos: "))
    ingresos_totales = int(input("Ingrese la cantidad de ingresos que desea generar: "))
    nombre_archivo = input("Ingrese el nombre del archivo JSON: ")
    ruta_escritorio = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    ingresos_generados = generar_ingresos(anio, ingresos_totales)
    datos_json = generar_json(ingresos_generados)
    guardar_json_en_archivo(datos_json, os.path.join(ruta_escritorio, f"{nombre_archivo}.json"))
    print(f"Archivo JSON guardado en el escritorio como '{nombre_archivo}.json'")

    # Calcular la diferencia entre la cantidad proporcionada y la cantidad generada
    diferencia = ingresos_totales - len(ingresos_generados)
    if diferencia != 0:
        print(f"Se agregaron {diferencia} ingresos adicionales para igualar la cantidad total.")

if __name__ == "__main__":
    main()

