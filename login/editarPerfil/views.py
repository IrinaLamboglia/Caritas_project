from django.shortcuts import render, redirect
from core.models import Usuario

def editar_perfil(request, correo):
    usuario = Usuario.objects.get(email=correo)
    if request.method == 'POST':
        # Procesar la edición del perfil
        # Redirigir a la página de perfil actualizado
        pass
    else:
        return render(request, 'editar_perfil.html', {'usuario': usuario})