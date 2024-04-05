# Importaciones 

from django.http import JsonResponse
import json
from io import StringIO
from datetime import datetime
import pandas as pd

#==================================================================================================
#=========================== CLASS ANALYZER CON MÉTODOS PARA NÁLISIS ==============================
#==================================================================================================
class Analyzer:
    def __init__(self):
        self.df = None
        self.context = {}
        self.columns_excluir = ["id_user","dInsertDate","acType", "Total_Gasto_Diario"]
        self.result_concepts = pd.DataFrame() # Df con conceptos en columnas sumados
        self.aggregated_df = pd.DataFrame()

    #=========================================================
    # MÉTODO CONVERTIR LOS DATOS RECUPERADOS DE SQL EN UN DF
    #=========================================================
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

    #================================================
    # MÉTODO CONVERTIR CONCEPTOS DE DF EN COLUMNAS
    #================================================
    def conv_concept(self):
        self.pivot_df = self.df.pivot_table(index = self.df.index, columns = 'szConcept', values = 'fValue', fill_value = 0)
        self.df_columns_index = self.df.drop(["szConcept", "fValue", "id"], axis=1)
        self.df_columns_index = self.df_columns_index.groupby(self.df_columns_index.index).first()
        self.aggregated_df = self.pivot_df.groupby(self.pivot_df.index).sum()
        self.aggregated_df = pd.merge(self.df_columns_index, self.aggregated_df, left_index=True,
                                       right_index=True, how='left')
        # Crear una lista de columnas para agrupar
        self.aggregated_df["Total_Gasto_Diario"] = self.aggregated_df[[col for col in self.aggregated_df if col not in self.columns_excluir]].sum(axis=1)
        return self.aggregated_df
    
    #=============================================
    # MÉTODO AGRUPAR POR CONCEPTOS Y SUMAR TOTAL 
    #=============================================
    def expenses_for_concept(self):
        # Crear una lista de columnas para agrupar
        self.concept_df = self.aggregated_df.drop(columns = self.columns_excluir)
        self.sum_column = self.concept_df.sum(axis=0).round(4)
        self.result_concepts = self.sum_column.to_dict()
        return self.result_concepts
    
    #==========================================
    # MÉTODO AGRUPAR IMPORTE TOTAL POR MESES 
    #==========================================
    def expenses_for_months(self):
        # Asegurarse de que el índice es de tipo DateTimeIndex
        if not isinstance(self.aggregated_df.index, pd.DatetimeIndex):
            self.aggregated_df.index = pd.to_datetime(self.aggregated_df.index)

        # Crear un DF con las columna acType y Total_Gasto_Diario
        self.aggregated_df2 = self.aggregated_df[["acType", "Total_Gasto_Diario"]]

        print(self.aggregated_df2.info())
        print(self.aggregated_df2)
        if len(self.aggregated_df2['acType'].unique()) == 1:
            self.acType_value = self.aggregated_df2['acType'].unique()[0]
            self.new_column_name = "Total Ingresos mensuales" if self.acType_value == "0001" else "Total Gastos mensuales"
            self.aggregated_df2 = self.aggregated_df2.rename(columns={"Total_Gasto_Diario": self.new_column_name})
        
        self.aggregated_df2['Month'] = self.aggregated_df2.index.to_period('M')
        self.monthly_totals = self.aggregated_df2.groupby('Month').sum()
        self.monthly_totals = self.monthly_totals.drop("acType", axis=1)
        print(self.monthly_totals)
        # print(self.aggregated_df.info())
        # Calcular el total mensual de gastos
        # self.monthly_totals['Total_Mensual'] = self.monthly_totals.sum(axis=1)
        return self.monthly_totals

    
    #===========================
    # MÉTODO PERIODO MAX Y MIN 
    #===========================
    def periodo(self):
        self.date_min = self.df.index.min()
        self.date_max = self.df.index.max()
        return self.date_min, self.date_max
    
    #===========================
    # GENERAR GRÁFICA 
    #===========================
    def graphic(self):
        pass
        
