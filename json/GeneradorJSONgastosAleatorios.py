import json
import os
import random
from datetime import datetime, timedelta

def generate_expenses(company_name):
    expenses = []

    # Gastos mensuales
    monthly_expenses = [
        {"concept": "Luz", "day": 5, "min_value": 50, "max_value": 200},
        {"concept": "Internet", "day": 15, "value": 80},
        {"concept": "Nominas", "day": 10, "value": 3000},
        {"concept": "Hipoteca", "day": 1, "value": 1000}
    ]

    # Gastos diarios
    daily_expenses = [
        {"concept": "Gasolina", "value": 30},
        {"concept": "Comida", "value": 20}
    ]

    # Gastos bimensuales
    bimonthly_expenses = [
        {"concept": "Agua", "value": 100},
        {"concept": "Seguro", "value": 200}
    ]

    # Gastos semestrales
    semiannual_expenses = [
        {"concept": "Seguro de coche", "value": 500}
    ]

    # Gastos anuales
    annual_expenses = [
        {"concept": "Suscripcion informatica", "value": 1000}
    ]

    # Generar gastos mensuales
    current_date = datetime(2015, 1, 1)
    end_date = datetime(2024, 12, 31)
    while current_date <= end_date and len(expenses) < 10000:
        for expense in monthly_expenses:
            if current_date.day == expense["day"]:
                if "value" in expense:
                    value = expense["value"]
                else:
                    value = random.randint(expense["min_value"], expense["max_value"])
                expenses.append({"concept": expense["concept"], "date": current_date.strftime("%d/%m/%Y"), "value": value})
        current_date += timedelta(days=1)

    # Generar gastos diarios
    current_date = datetime(2015, 1, 1)
    while current_date <= end_date and len(expenses) < 10000:
        for expense in daily_expenses:
            expenses.append({"concept": expense["concept"], "date": current_date.strftime("%d/%m/%Y"), "value": expense["value"]})
        current_date += timedelta(days=1)

    # Generar gastos bimensuales
    current_date = datetime(2015, 1, 1)
    while current_date <= end_date and len(expenses) < 10000:
        for expense in bimonthly_expenses:
            if current_date.month % 2 == 0 and current_date.day == 1:
                expenses.append({"concept": expense["concept"], "date": current_date.strftime("%d/%m/%Y"), "value": expense["value"]})
        current_date += timedelta(days=1)

    # Generar gastos semestrales
    current_date = datetime(2015, 1, 1)
    while current_date <= end_date and len(expenses) < 10000:
        for expense in semiannual_expenses:
            if current_date.month in [1, 7] and current_date.day == 1:
                expenses.append({"concept": expense["concept"], "date": current_date.strftime("%d/%m/%Y"), "value": expense["value"]})
        current_date += timedelta(days=1)

    # Generar gastos anuales
    current_date = datetime(2015, 1, 1)
    while current_date <= end_date and len(expenses) < 10000:
        for expense in annual_expenses:
            if current_date.month == 1 and current_date.day == 1:
                expenses.append({"concept": expense["concept"], "date": current_date.strftime("%d/%m/%Y"), "value": expense["value"]})
        current_date += timedelta(days=1)

    # Truncar la lista si excede los 10000 gastos
    expenses = expenses[:10000]

    # Ordenar los gastos por fecha
    expenses.sort(key=lambda x: datetime.strptime(x["date"], "%d/%m/%Y"))

    return expenses

def generate_json(company_name):
    expenses = generate_expenses(company_name)

    json_data = {
        "szName": company_name,
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
    company_name = input("Ingrese el nombre de la empresa: ")
    filename = input("Ingrese el nombre del archivo JSON: ")

    json_data = generate_json(company_name)
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, f"{filename}.json")
    save_json_to_file(json_data, file_path)
    print(f"Archivo JSON guardado en el escritorio como '{filename}.json'")

if __name__ == "__main__":
    main()

