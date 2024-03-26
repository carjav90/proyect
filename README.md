PROYECTO ANALISIS DE DATOS DE CONCILIACION BANCARIA

** PASOS PARA EL DESARROLLO DE LA APLICACION **

A.- INSERCCION Y MANIPULACION INICIAL DE DATOS
  1 Generar archivo JSON aleatorio con Gastos e Ingresos
  
  2 Desarrollar codigo para poder insertar varios archivos JSON tanto en gastos como en Ingresos
  
    2.1 En el entorno Web poder seleccionar que tipo de JSON es si es Gastos o Ingresos a la hora de insertar el archivo
    -- Esto debe de ser obligatorio a la hora de insertar el archivo, si no no nos dejará insertarlo --
    
  3 Unificar los archivos insertados en Gastos e Ingresos
  
  4 Dividir el JSON de GAstos e Ingresos por conceptos.
  
    4.1 Agrupar por conceptos y periodos de pagos o cobros para saber la periocidad de dichos datos
    
  5 Generar 2 JSON sin agrupar por:
  
    5.1 Ingresos Fijos
    
    5.2 Ingresos Otros
    
  6 Generar 3 JSON sin agrupar por:
  
    6.1 Gastos fijos
    
    6.2 Gastos variables o inusuales
    
    6.3 Gastos a largo plazo.
    
B.- ENTORNO WEB CON DJANGO

  1 Crear aplicacion en Django
  
  2 Preparar base de datos en Modelo
  
  3 Crear las URLS necesarias para nuestra web
  
  4 Crear nuestra lógica en Views.py

  5 Representación de datos con PowerBi


C.- VISUALIZACIÓN DE REPORTE

  1 Crear PowerBi donde el cliente pueda seleccionar el algoritmo de pronóstico

  2 Entorno donde se pueda elegir los periodos y datos a reportar.
