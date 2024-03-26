import json
import os
import random
from datetime import datetime, timedelta

def generar_gastos_empresa(tipo_empresa):
    gastos = []

    # Diccionario de tipos de gastos y sus periodos
    tipos_gastos = {
        "luz": "mensual",
        "internet": "mensual",
        "gasolina": "mensual",
        "comida": "mensual",
        "papel": "mensual",
        "cafe": "mensual",
        "agua": "bi-mensual",
        "seguro": "bi-mensual",
        "seguro_coche": "semestral",
        "escritorio": "anual"
    }

    # Definir rangos de fechas
    fecha_inicio = datetime(2015, 1, 1)
    fecha_fin = datetime(2024, 12, 31)

    # Generar gastos
    for _ in range(10000):
        concepto = random.choice(list(tipos_gastos.keys()))
        periodo = tipos_gastos[concepto]
        fecha_gasto = fecha_inicio + timedelta(days=random.randint(0, (fecha_fin - fecha_inicio).days))
        cantidad = round(random.uniform(50, 5000), 2)

        gastos.append({
            "fecha": fecha_gasto.strftime("%Y-%m-%d"),
            "concepto": concepto,
            "cantidad": cantidad
        })

    return gastos

def preguntar_tipo_empresa():
    tipo_empresa = input("Por favor, introduzca el tipo de empresa: ")
    return tipo_empresa

def preguntar_nombre_archivo():
    nombre_archivo = input("Por favor, introduzca el nombre del archivo: ")
    return nombre_archivo

def guardar_json_en_escritorio(datos, nombre_archivo):
    ruta_archivo = os.path.join(os.path.expanduser("~"), "Desktop", f"{nombre_archivo}.json")
    with open(ruta_archivo, "w") as archivo:
        json.dump(datos, archivo, indent=4)
    print(f"Archivo guardado en {ruta_archivo}")

def main():
    tipo_empresa = preguntar_tipo_empresa()
    gastos = generar_gastos_empresa(tipo_empresa)
    nombre_archivo = preguntar_nombre_archivo()
    guardar_json_en_escritorio(gastos, nombre_archivo)

if __name__ == "__main__":
    main()

 
