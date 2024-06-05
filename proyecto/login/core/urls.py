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
from .views import home,products,exit
from . import views


urlpatterns = [
    path('', home, name='home'),
    path('products/', products,name='products'),
    path('logout/',exit, name='exit'),
    path('accounts/login/', views.login_nuevo , name='login'),
    path('registro/', views.formularioreg, name='registro'),  # URL para el formulario de registro
    path('login_ayudante/', views.procesar_clave, name="login_ayudante"),
    path('bajaAyudante/',views.mostrarBaja,name='mostrarBaja'),
    path('eliminarAyudante/<str:email>/', views.eliminarAyudante, name='eliminarAyudante'),
  #  path('accounts/login/<email>/', views.recuperarCuenta, name='recuperarCuenta'), #no anda y no lo tenia q hacer lpm
    path('listado/bloqueadosListado/',views.listadoBloqueado, name='listadoBloqueados')

]
