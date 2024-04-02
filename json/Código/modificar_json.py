import pandas as pd
import json
from datetime import datetime

# Cargar los datos desde el archivo JSON
file_path = 'C:/Users/borja/Desktop/Impactware/App_analisis_datos_impactware/proyect/json/ingresos2021.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Convertir los datos a un DataFrame de Pandas
fields = data['lszFields']
values = data['lkValues']
df = pd.DataFrame(values, columns=fields)

# Agregar las nuevas columnas y asignar los valores correspondientes
df['id_user'] = 306  # Asignar el mismo valor a toda la columna
df['dInsertDate'] = datetime.now().strftime('%d/%m/%Y')  # Fecha de hoy en formato dd/mm/yyyy
df['acType'] = '0001'  # Asignar un valor fijo a toda la columna

# Reordenar las columnas según el orden especificado
ordered_columns = ['id_user', 'dInsertDate', 'dDate', 'szConcept', 'fValue', 'acType']
df = df[ordered_columns]

# Convertir de nuevo a formato JSON
modified_data = {
    "szName": data['szName'],
    "lszFields": ordered_columns,
    "lkValues": df.values.tolist()
}

# Guardar el nuevo JSON en un archivo
new_file_path = 'C:/Users/borja/Desktop/Impactware/App_analisis_datos_impactware/proyect/json/modified_ingresos2021.json'
with open(new_file_path, 'w') as file:
    json.dump(modified_data, file, indent=4)

new_file_path

