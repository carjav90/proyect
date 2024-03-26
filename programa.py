import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from pandas.tseries.offsets import DateOffset
from statsmodels.tsa.statespace.sarimax import SARIMAX
import statsmodels.api as sm
import holidays
import matplotlib.dates as mdates

def leer_datos(archivo):
     df = pd.read_csv(archivo, delimiter=";",index_col='Mes')
     df.index = pd.to_datetime(df.index)   
     return df

def prever_futuro(df):
    # Predicción
    df['es_fin_de_semana'] = (df.index.weekday >= 5)
    dias_festivos = holidays.Spain()
    df['es_festivo'] = df.index.isin(dias_festivos)
    modelo = sm.tsa.statespace.SARIMAX(df['Ingresos'], order = (2,1,2), seasonal_order = (3,1,1,12))
    resultado = modelo.fit()
    print(resultado.summary())
    fig, axs =plt.subplots(3,1, figsize=(7,7))
    
    # Grafica residuos
    axs[0].set_xlabel('Año')
    axs[0].set_ylabel('Cantidad')
    axs[0].set_title('Residuos')
    axs[0].legend(loc='upper left')
    resultado.resid.plot(ax=axs[0])
    
    # Grafica predicciones
    df['pronostico'] = resultado.predict()
    df[['Ingresos','pronostico']].plot(ax=axs[1])
    axs[1].set_title('Predicción')
    axs[1].legend(loc='upper left')
    axs[1].grid(True)
    fechasfuturas = [df.index[-1] + DateOffset(months = x) for x in range(1,13)]
    df_futura = pd.DataFrame(index = fechasfuturas, columns= df.columns)
    nuevodf=pd.concat([df,df_futura])
    nuevodf['pronostico']=resultado.predict(start =156, end=180)
    
    # Grafica futura
    nuevodf[['Ingresos', 'pronostico']].plot(ax=axs[2])
    axs[2].set_xlabel('Año')
    axs[2].set_ylabel('Cantidad')
    axs[2].set_title('Predicción Futura')
    sns.set_style("darkgrid")
    axs[2].legend(loc='upper left')
    axs[2].grid(True)
    plt.tight_layout()
    plt.show()
    
    ultimo_año = df.index.max().year
    plt.figure(figsize=(7,7))
    # Predicción pesimista
    plt.subplot(2, 1, 1)
    prediccion_pesimista = resultado.get_prediction(start=pd.to_datetime(f'{ultimo_año}-01-01'), dynamic=False)
    prediccion_pesimista_ci = prediccion_pesimista.conf_int()
    plt.plot(df.index, df['Ingresos'], label='Ingresos observados')
    plt.plot(prediccion_pesimista.predicted_mean.index, prediccion_pesimista.predicted_mean, color='red', label='Predicción pesimista')
    plt.fill_between(prediccion_pesimista_ci.index, prediccion_pesimista_ci.iloc[:, 0], prediccion_pesimista_ci.iloc[:, 1], color='red', alpha=0.2)
    plt.title('Predicción Pesimista')
    plt.xlabel('Fecha')
    plt.ylabel('Ingresos')
    plt.legend(loc='upper left', fontsize='small')
    plt.grid(True)


    # Predicción optimista
    plt.subplot(2, 1, 2)
    prediccion_optimista = resultado.get_prediction(start=pd.to_datetime(f'{ultimo_año}-01-01'), dynamic=False)
    prediccion_optimista_ci = prediccion_optimista.conf_int()
    plt.plot(df.index, df['Ingresos'], label='Ingresos observados')
    plt.plot(prediccion_optimista.predicted_mean.index, prediccion_optimista.predicted_mean, color='green', label='Predicción optimista')
    plt.fill_between(prediccion_optimista_ci.index, prediccion_optimista_ci.iloc[:, 0], prediccion_optimista_ci.iloc[:, 1],
                    color='green', alpha=0.2)
    plt.title('Predicción Optimista')
    plt.xlabel('Fecha')
    plt.ylabel('Ingresos')
    plt.legend(loc='upper left', fontsize='small')
    plt.grid(True)
    plt.tight_layout()  
    plt.show()


def comparar_gastos(df, año, mes=None):
    if mes is None:
       df_año = df[df.index.year == int(año)]
       df_melt = df_año.melt(value_vars=['Gastos', 'Gastos_Imprevistos'], ignore_index=False)
    else:
        df_mes = df[(df.index.year == int(año)) & (df.index.month == int(mes))]
        df_melt = df_mes.melt(value_vars=['Gastos', 'Gastos_Imprevistos'], ignore_index=False)
    
    sns.barplot(x=df_melt.index, y=df_melt.value, hue='variable', data=df_melt)
    plt.title('Comparacion de Gastos Imprevistos')
    plt.xlabel('Fecha')
    plt.ylabel('Valor')
    plt.legend(loc='upper left')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()


def main():
    archivo = input("Introduce el nombre del Archivo CSV: ")
    df = leer_datos(archivo)
    
    while True:
        print("\nSeleccione una Opción:")
        print("1. Hacer una Previsión a Futuro de la Empresa")
        print("2. Comparar Gastos y Gastos Imprevistos por Año")
        print("3. Comparar Gastos y Gastos Imprevistos por Mes")
        print("4. Salir")
        opcion = input("Elige una Opción: ")

        if opcion == '1':
            prever_futuro(df)
        elif opcion == '2':
            año = input("Introduzca el Año a Comparar: ")
            comparar_gastos(df,año)
        elif opcion == '3':
            año = input("Introduzca el Año: ")
            mes = input("Introduzca el Numero del Mes a Comparar: ")
            comparar_gastos(df,año,mes)
        elif opcion == '4':
            print("Hasta Luego")
            break
        else:
            print("Opción no válida. Por favor, Intenta de Nuevo.")

if __name__ == "__main__":
    main()