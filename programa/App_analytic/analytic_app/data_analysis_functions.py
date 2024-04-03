# Importaciones 

from django.http import JsonResponse
import json
from io import StringIO
from datetime import datetime
import pandas as pd

class Analyzer:
    def __init__(self):
        self.df = None
        self.context = {}

    # Método que convierta los datos recuperados de SQL en df
    def conv_json_df(self, datos):
        if 'error' in datos:
            self.context = {"error": datos["error"]}
        else:
            # Formatear las fechas antes de pasar los datos a la plantilla
            for desc in datos:

                # Convierte los datos de las ferchas a Strings para que se puedan introducir en el JSON con el resto de datos           
                # Para 'dDate'
                if isinstance(desc['dDate'], dict) and 'date' in desc['dDate']:
                    fecha_str = desc['dDate']['date']
                    fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S.%f')
                    desc['dDate'] = fecha_obj.strftime('%Y-%m-%d')  # Formato simplificado para 'dDate'
                
                # Para 'dInsertDate'
                if isinstance(desc['dInsertDate'], dict) and 'date' in desc['dInsertDate']:
                    fecha_insert_str = desc['dInsertDate']['date']
                    fecha_insert_obj = datetime.strptime(fecha_insert_str, '%Y-%m-%d %H:%M:%S.%f')
                    desc['dInsertDate'] = fecha_insert_obj.strftime('%Y-%m-%d')  # Formato simplificado para 'dInsertDate'
            
            # Serializacion de los datos en JSON
            datos_json = json.dumps(datos)
            datos_json_io = StringIO(datos_json)
            self.df = pd.read_json(datos_json_io, dtype={'acType': 'str'})

            # Convertir las fechas a formato datetime, si no lo están
            self.df['dDate'] = pd.to_datetime(self.df['dDate'])
            self.df['dInsertDate'] = pd.to_datetime(self.df['dInsertDate'])

            # Asegúrate de que las fechas estén en el formato correcto
            self.df['dDate'] = self.df['dDate'].dt.strftime('%Y-%m-%d')
            self.df['dInsertDate'] = self.df['dInsertDate'].dt.strftime('%Y-%m-%d')
            self.df.sort_values(by="dDate", inplace = True)# Ordenar por la columna dDate
            datos_ordenados = self.df.to_dict('records')

            # Convierte dDate en el indice del df
            self.df.set_index("dDate", inplace=True)
            
            # Ordena los registros por fechas de los conceptos
            self.df.sort_values(by="dDate", inplace = True)# Ordenar por la columna dDate
            

            # Suma de la columna fValue y redondeo de a 2 decimales
            suma = round(self.df['fValue'].sum(), 2)
            print(self.df)

            # Contar nº de registros
            count = self.df["szConcept"].count()
            context = {"Description": datos_ordenados,
                        "Resultado_Suma": suma,
                        "n_de_registros": count}
            
            return context


    # Método convertir conceptos del df en columnas 
    def conv_concept(self):
        if self.df is not None:
            print(self.df.head())
        else:
            print("Dataframe no esta definido")

    
