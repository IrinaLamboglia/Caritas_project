"""login URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path 
from .views import home,products
from log_out.views import confirmar_salida,exit
#importo funcion exit
from . import views


urlpatterns = [
    path('', home, name='home'),
    path('products/', products,name='products'),
    path('logout/',exit, name='exit'),
    path('accounts/login/', views.login_nuevo , name='login'),
    path('registro/', views.formularioreg, name='registro'),  # URL para el formulario de registro
    path('login_ayudante/', views.procesar_clave, name="login_ayudante"),
   # path('bajaAyudante/',views.bajaAyudante,name='bajaAyudante'), #la tengo q hacer 
    path('bajaAyudante/',views.mostrarBaja,name='mostrarBaja'),
    path('confirmar_salida/', confirmar_salida, name='confirmar_salida'),
]
