
import json
import random
from datetime import datetime, timedelta
import os

def generate_incomes():
    incomes = []

    # Ingresos mensuales
    monthly_incomes = [
        {"concept": "Subscripcion mensual", "day": 5, "min_value": 1000, "max_value": 5000, "added": False}
    ]

    # Ingresos trimestrales
    quarterly_incomes = [
        {"concept": "Subscripcion trimestral", "day": 5, "value": 2000, "added": False}
    ]

    # Ingresos semestrales
    semiannual_incomes = [
        {"concept": "Subscripcion semestral", "day": 5, "value": 3000}
    ]

    # Ingresos anuales
    annual_incomes = [
        {"concept": "Subscripcion anual", "day": 5, "value": 5000}
    ]

    # Generar ingresos mensuales
    current_date = datetime(2015, 1, 1)
    end_date = datetime(2024, 12, 31)
    while current_date <= end_date and len(incomes) < 1000000:
        for income in monthly_incomes:
            if current_date.day == income["day"] and not income["added"]:
                value = round(random.uniform(income["min_value"], income["max_value"]), 2)
                incomes.append({"concept": income["concept"], "date": current_date.strftime("%d/%m/%Y"), "value": value})
                income["added"] = True
        current_date += timedelta(days=1)

    # Generar ingresos trimestrales
    current_date = datetime(2015, 1, 1)
    while current_date <= end_date and len(incomes) < 1000000:
        for income in quarterly_incomes:
            if current_date.day == income["day"] and current_date.month % 3 == 0 and not income["added"]:
                incomes.append({"concept": income["concept"], "date": current_date.strftime("%d/%m/%Y"), "value": income["value"]})
                income["added"] = True
        current_date += timedelta(days=1)

    # Generar ingresos semestrales
    current_date = datetime(2015, 1, 1)
    while current_date <= end_date and len(incomes) < 1000000:
        for income in semiannual_incomes:
            if current_date.day == income["day"] and current_date.month % 6 == 0:
                incomes.append({"concept": income["concept"], "date": current_date.strftime("%d/%m/%Y"), "value": income["value"]})
        current_date += timedelta(days=1)

    # Generar ingresos anuales
    current_date = datetime(2015, 1, 1)
    while current_date <= end_date and len(incomes) < 1000000:
        for income in annual_incomes:
            if current_date.day == income["day"] and current_date.month == 1:
                incomes.append({"concept": income["concept"], "date": current_date.strftime("%d/%m/%Y"), "value": income["value"]})
        current_date += timedelta(days=1)

    # Ingresos diarios
    daily_incomes = [{"concept": f"Articulo {i}", "value": random.uniform(10, 100)} for i in range(1, 101)]
    current_date = datetime(2015, 1, 1)
    while current_date <= end_date and len(incomes) < 1000000:
        if current_date.weekday() != 6:
            for income in daily_incomes:
                if random.random() < 0.2:  # Simulando ventas diarias
                    incomes.append({"concept": income["concept"], "date": current_date.strftime("%d/%m/%Y"), "value": income["value"]})
        current_date += timedelta(days=1)

    # Truncar la lista si excede los 1000000 ingresos
    incomes = incomes[:1000000]

    return incomes

def generate_json():
    incomes = generate_incomes()

    json_data = {
        "szName": "Empresa",
        "lszFields": [
            "szConcept",
            "dDate",
            "fValue"
        ],
        "lkValues": [[income["concept"], income["date"], income["value"]] for income in incomes]
    }

    return json_data

def save_json_to_file(json_data, filename):
    with open(filename, 'w') as f:
        json.dump(json_data, f, indent=4)

def main():
    filename = input("Ingrese el nombre del archivo JSON: ")
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    json_data = generate_json()
    save_json_to_file(json_data, os.path.join(desktop_path, f"{filename}.json"))
    print(f"Archivo JSON guardado en el escritorio como '{filename}.json'")

if __name__ == "__main__":
    main()
