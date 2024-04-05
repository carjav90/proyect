"""
URL configuration for App_analytic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from analytic_app.views import reporte, envio_datos, envio_json, time_series

urlpatterns = [
    path('admin/', admin.site.urls),
    path('recibir/', reporte, name='home'),  # Esto manejará la URL raíz,
    path('enviar/', envio_datos, name='envio'), 
    path('enviar2/', envio_json, name='envioJson'),  
    path("time_series/", time_series, name = 'series_tiempo'),
]

