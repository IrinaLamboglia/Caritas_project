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
from log_out.views import exit
#importo funcion exit
from . import views
from editarPerfil.views import editar_ayudante
from agregarCategoria.views import agregar_categoria, mostrar_categorias
from bajaCategoria.views import  desactivar_categoria
from listarprod.views import mostrar_validacion,aceptar_publicacion,rechazar_publicacion,bloquear_usuario
from django.urls import path




urlpatterns = [
    path('', home, name='home'),
    path('products/', products,name='products'),
    path('logout/',exit, name='exit'),
    path('accounts/login/', views.login_nuevo , name='login'),
    path('registro/', views.formularioreg, name='registro'),  
    
    path('login_ayudante/', views.procesar_clave, name="login_ayudante"),

   # path('bajaAyudante/',views.bajaAyudante,name='bajaAyudante'), #la tengo q hacer 
    path('sobreNosotros/',views.editar_sobre_nosotros,name='editarSobreNosotros'),
    path('bajaAyudante/',views.mostrarBaja,name='mostrarBaja'),
    #path('confirmar_salida/', confirmar_salida, name='confirmar_salida'),
    
    
    path('eliminarAyudante/<str:email>/', views.eliminarAyudante, name='eliminarAyudante'),
    # URL para la edición de perfil del ayudante
    path('editar_perfil/<int:id>/', editar_ayudante, name='editar_ayudante'),
   
    path('listado/bloqueadosListado/',views.listadoBloqueado, name='listadoBloqueados'),
    
    path('agregar_categoria/', agregar_categoria, name='agregar_categoria'),
    
    path('categoria/', mostrar_categorias, name='mostarCategoria'),

   # path('categoria/<int:categoria_id>/', bajar_categoria, name='bajarCategoria'),
    path('inicio/', home, name='inicio'),
    path('accounts/login/<email>/', views.recuperarCuenta, name='recuperarCuenta'), 
    
    path('crearPublicacion/',views.crear_publicacion, name='crear_publicacion'),
    path('ver/<int:publicacion_id>/',views.ver_producto, name='ver_producto'),




    path('desbloquear/<str:email>/', views.desbloquearUsuario, name='desbloquear_usuario'),
    path('mis_publicaciones/', views.mis_publicaciones, name='mis_publicaciones'),
    #ESTO ES NUEVO
    path('eliminar_publicacion/<int:publicacion_id>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('mostrarValidacion/', mostrar_validacion, name='mostrar_validacion'),
    path('aceptarPublicacion/<int:id>/', aceptar_publicacion, name='aceptar_publicacion'),
    path('rechazarPublicacion/<int:id>/', rechazar_publicacion, name='rechazar_publicacion'),
    path('bloquearUsuario/<int:id>/', bloquear_usuario, name='bloquear_usuario'),

     path('categoria/desactivar/<int:categoria_id>/', desactivar_categoria, name='desactivar_categoria'),




    path('check_email/', views.check_email, name='check_email'),
    path('misTrueques/', views.ver_misTrueques, name='misTrueques'),

     path('solicitar-trueque/<int:publicacion_id>/', views.solicitar_trueque, name='solicitar_trueque'),
    path('registrar-solicitud/<int:publicacion_objetivo_id>/', views.registrar_solicitud, name='registrar_solicitud'),
    path('filtro/misTrueques/',views.filtro_trueques,name='filtro_trueques'),
    path('truequesAdmin/',views.trueques_realizados,name='trueques_realizados')


]
