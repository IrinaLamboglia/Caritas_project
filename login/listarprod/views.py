from django.shortcuts import render, redirect
from core.models import Publicacion, Usuario, UsuarioBloqueado

def mostrar_validacion(request):
    publicaciones_a_validar = Publicacion.objects.filter(estado=False,categoria=None)
    return render(request, 'validacion/mostrar_validacion.html', {'publicaciones_a_validar': publicaciones_a_validar})

def aceptar_publicacion(request, id):
    publicacion = Publicacion.objects.get(id=id)
    publicacion.estado = True
    publicacion.save()
    return redirect('mostrar_validacion')

def rechazar_publicacion(request, id):
    publicacion = Publicacion.objects.get(id=id)
    publicacion.delete()
    return redirect('mostrar_validacion')

def bloquear_usuario(request, id):
    usuario = Usuario.objects.get(id=id)
    if not UsuarioBloqueado.objects.filter(email=usuario.email).exists():  # Verificar si el usuario no está ya bloqueado
        publicaciones_usuario = Publicacion.objects.filter(usuario=usuario)
        for publicacion in publicaciones_usuario:
            publicacion.delete()
        UsuarioBloqueado.objects.create(email=usuario.email) 
    return redirect('mostrar_validacion')
