import json

def cargar_datos_desde_json(archivo):
    with open(archivo, 'r') as f:
        return json.load(f)

def calcular_balance(archivo_ingresos, archivo_gastos):
    # Cargar datos de ingresos y gastos desde archivos JSON
    ingresos = cargar_datos_desde_json(archivo_ingresos)['lkValues']
    gastos = cargar_datos_desde_json(archivo_gastos)['lkValues']

    # Calcular suma de ingresos por año
    ingresos_por_año = {}
    for transaccion in ingresos:
        fecha = transaccion[1]
        año = fecha[-4:]  # Obtiene los últimos 4 caracteres que corresponden al año
        monto = transaccion[2]
        ingresos_por_año[año] = ingresos_por_año.get(año, 0) + monto

    # Calcular suma de gastos por año
    gastos_por_año = {}
    for transaccion in gastos:
        fecha = transaccion[1]
        año = fecha[-4:]  # Obtiene los últimos 4 caracteres que corresponden al año
        monto = transaccion[2]
        gastos_por_año[año] = gastos_por_año.get(año, 0) + monto

    # Calcular balance por año
    balance_por_año = {}
    for año in set(ingresos_por_año.keys()) | set(gastos_por_año.keys()):
        balance_por_año[año] = round(ingresos_por_año.get(año, 0) - gastos_por_año.get(año, 0), 2)

    # Mostrar resultado
    print("Balance por año:")
    for año, balance in balance_por_año.items():
        if balance > 0:
            estado = "Positivo"
        else:
            estado = "Deficitario"
        print(f"Año {año}: {balance} ({estado})")

# Rutas de los archivos de ingresos y gastos en formato JSON
archivo_ingresos = 'ingresos.json'
archivo_gastos = 'gastos.json'

# Llamar a la función para calcular el balance
calcular_balance(archivo_ingresos, archivo_gastos)
