PROYECTO ANALISIS DE DATOS DE CONCILIACION BANCARIA

** PASOS PARA EL DESARROLLO DE LA APLICACION **

A.- INSERCCION Y MANIPULACION INICIAL DE DATOS

  1 Generar archivo JSON aleatorio con Gastos e Ingresos **HECHO**
  
  2 Desarrollar codigo para poder insertar varios archivos JSON o url en tabla tbDataInsert **HECHO**
  
    2.1 En el entorno Web poder seleccionar que tipo de JSON es si es Gastos o Ingresos a la hora de insertar el archivo. 
    NOTA: EL JSON VIENE POR POSTMAN EN LOS DATOS O ACCEDIENDO NOSOTROS A UNA URL**. 
    
    -- Para distinguir que tipo de dato es esta el campo acType --
    
  3 Insertar los datos en la DBaibf en la tbDataInsert **HECHO**
  
  4 Dividir el JSON de GAstos e Ingresos por conceptos. **HECHO**
    NOTA: Los datos ya vienen separados por acType
  
    4.1 Agrupar por conceptos y periodos de pagos o cobros para saber la periodicidad de dichos datos
    
  5 Generar 2 JSON sin agrupar por:
  
    5.1 Ingresos Fijos
    
    5.2 Ingresos Otros

    5.3 Agrupar los registros por meses
    
  6 Generar 3 JSON sin agrupar por:
  
    6.1 Gastos fijos
    
    6.2 Gastos variables o inusuales
    
    6.3 Gastos a largo plazo.

    5.4 Agrupar los registros por meses

  7 Crear lógica de análisis

    7.1 Crear el df, con las columnas correspondientes y con el index = datetime
    -- Entrar en detalle en otro momento de los datos que tenemos que analizar y los resultados que tenemos que obtener para los posteriores modelos. --

    7.2 Modelo con statsmodels para Análisis con periodos de tiempo
    
      7.2.1 Media movil

      7.2.2 Representación estacional en los periodos de 1, 3, 6, 12 meses
        -- PAra poder visualizar graficas si el cliente lo pide --

      7.2.3 Prueba de Dickey-Fuller busca determinar si una serie de tiempo es estacionaria o no . La hipótesis nula de esta prueba es que la serie de tiempo no es estacionaria.
      -- Hacer la logica para ver si el valor de p-value es mayor a 0.05 y si es asi hacer diferencias y volver a hacer la prueba hasta que p-value < 0.05 --
      7.2.4 Partir los datos quitando los ultimos 12 registros y dejando un df de gastosA y gastosB, ingresosA, ingresosB

      7.2.5 ¿Como analizar la gráfica de ACF (autocorrelacion) y de PACF (Autocorrelación Parcial)?

      7.2.6 Crear modelo SARIMAX con from statsmodels.tsa.arima_model import ARIMA
      -- order = (q,Q,p) seasonal_order = (P,d,D,S) S es el periodo estacional que puede ser 1, 3, 6, 12 meses
      
      7.2.7 Entrenamiento del modelo model.fit()

      7.2.8 Crear predicciones y gráficas a partir de los resultados para los datos que tenemos sin datos futuros

      7.2.9 Crear columnas en df con fechas futuras para generar el pronostico desde la prediccion del modelo.
      -- Concatenamos el df con los datos de pronostico y el df futuro sin datos
      -- Predeccior resultados con resultados.predict() para 3, 6, 12, 24 meses

      

    
    
B.- ENTORNO WEB CON DJANGO

  1 Crear aplicacion en Django
  
  2 Preparar base de datos en Modelo
  
  3 Crear las URLS necesarias para nuestra web
  
  4 Crear nuestra lógica en Views.py

  5 Representación de datos


C.- VISUALIZACIÓN DE REPORTE

  1 Crear Entorno con Html y CSS con Script de Javascript

  2 Entorno donde se pueda elegir los periodos y datos a reportar.

