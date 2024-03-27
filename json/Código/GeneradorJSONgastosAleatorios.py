import json
import os
import random
from datetime import datetime, timedelta

def generar_gastos(ano):
    expenses = []

    # Gastos mensuales
    gastos_mensuales = [
        {"concept": "Luz", "day": 5, "min_value": 50, "max_value": 200},
        {"concept": "Internet", "day": 15, "value": 80},
        {"concept": "Nominas", "day": 10, "value": 19000},
        {"concept": "Hipoteca", "day": 1, "value": 2500}
    ]

    # Gastos diarios
    gastos_diarios = [
        {"concept": "Gasolina", "min_value": 25, "max_value": 120},
        {"concept": "Comida", "min_value": 10, "max_value": 30}
    ]

    # Generar gastos mensuales
    current_date = datetime(ano, 1, 1)
    end_date = datetime(ano, 12, 31)
    while current_date <= end_date:
        for expense in gastos_mensuales:
            if current_date.day == expense.get("day"):
                if "value" in expense:
                    value = expense["value"]
                else:
                    value = random.randint(expense["min_value"], expense["max_value"])
                expenses.append({"concept": expense["concept"], "date": current_date.strftime("%d/%m/%Y"), "value": value})
        current_date += timedelta(days=1)

    # Generar gastos diarios
    current_date = datetime(ano, 1, 1)
    gasolina_count = 0
    comida_count = 0
    while current_date <= end_date:
        for expense in gastos_diarios:
            if expense["concept"] == "Comida":
                if comida_count < 15:  # Distribuir aleatoriamente hasta 15 veces al mes
                    if random.random() < 15/30:  # Probabilidad de aparición en cada día del mes
                        expenses.append({"concept": expense["concept"], "date": current_date.strftime("%d/%m/%Y"), "value": round(random.uniform(expense["min_value"], expense["max_value"]), 2)})
                        comida_count += 1
            elif expense["concept"] == "Gasolina":
                if gasolina_count < 7:  # Distribuir aleatoriamente hasta 7 veces al mes
                    if random.random() < 7/30:  # Probabilidad de aparición en cada día del mes
                        expenses.append({"concept": expense["concept"], "date": current_date.strftime("%d/%m/%Y"), "value": round(random.uniform(expense["min_value"], expense["max_value"]), 2)})
                        gasolina_count += 1
        current_date += timedelta(days=1)

    # Truncar la lista si excede los 10000 gastos
    expenses = expenses[:10000]

    # Ordenar los gastos por fecha
    expenses.sort(key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y"))

    return expenses

def generate_json(ano):
    expenses = generar_gastos(ano)

    json_data = {
        "szName": "expenses",
        "lszFields": [
            "szConcept",
            "dDate",
            "fValue"
        ],
        "lkValues": [[expense["concept"], expense["date"], expense["value"]] for expense in expenses]
    }

    return json_data

def save_json_to_file(json_data, filename):
    with open(filename, 'w') as f:
        json.dump(json_data, f, indent=4)

def main():
    
    filename = input("Ingrese el nombre del archivo JSON: ")
    ano = int(input("¿Para qué año desea que se generen los gastos? "))

    json_data = generate_json(ano)
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, f"{filename}.json")
    save_json_to_file(json_data, file_path)
    print(f"Archivo JSON guardado en el escritorio como '{filename}.json'")

    total_gastos = sum(expense[2] for expense in json_data["lkValues"])  # Acceder al tercer elemento de cada lista
    print(f"El total de todos los gastos es: {total_gastos}")

if __name__ == "__main__":
    main()

