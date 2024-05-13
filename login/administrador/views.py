from django.core.mail import send_mail
from django.shortcuts import render, redirect
from core.models import Administrador
from django.contrib import messages

def alta(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre_usuario = request.POST.get('email')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        telefono = request.POST.get('telefono')
        contraseña = request.POST.get('contraseña')
        dni = request.POST.get('dni')
        filial = request.POST.get('filial')

        # Verificar si ya existe un ayudante en la misma filial
        if Administrador.objects.filter(filial=filial).exists():
            # Si ya existe, mostrar un mensaje de error o tomar alguna acción
            mensaje_error = "No se puede registrar, ya existe un ayudante registrado en esta filial."
            return render(request, 'admin/alta.html', {'mensaje_error': mensaje_error})
        else:
            if Administrador.objects.filter(nombre_usuario=nombre_usuario).exists():
                mensaje_error="No se puede registrar, ya esta registrado como usuario"
                return render(request, 'admin/alta.html', {'mensaje_error': mensaje_error})
            else:
                # Verificar la longitud de la contraseña
                if len(contraseña) < 6:
                    mensaje_error = "La contraseña debe tener al menos 6 caracteres."
                    return render(request, 'admin/alta.html', {'mensaje_error': mensaje_error})
                else:
                    # Si no existe, crear un nuevo ayudante
                    nuevo_ayudante=Administrador.objects.create(
                        nombre_usuario=nombre_usuario,
                        nombre=nombre,
                        apellido=apellido,
                        fecha_nacimiento=fecha_nacimiento,
                        telefono=telefono,
                        contraseña=contraseña,
                        dni=dni,
                        filial=filial
                    )
                    # Enviar el correo al ayudante
                    enviar_correo_ayudante(nuevo_ayudante)
                    # Mostrar el mensaje de éxito
                    mensaje_exito= "Se mando el email al ayudante con sus datos y se registraron los datos exitosamente."
                    return render(request,'admin/alta.html',{'mensaje_exito':mensaje_exito})
        # Si la solicitud no es POST, simplemente renderiza el formulario
    return render(request, 'admin/alta.html')

def enviar_correo_ayudante(ayudante):
    asunto = "Bienvenido a nuestra plataforma"
    mensaje = f"¡Hola {ayudante.nombre} {ayudante.apellido}! Te hemos registrado en nuestra plataforma como ayudante. Te enviamos tu informacion para que puedas iniciar sesion: Nombre de usuario: {ayudante.nombre_usuario} y la contraseña:{ayudante.contraseña}. Saludos."
    correo_destino = ayudante.nombre_usuario
    send_mail(asunto, mensaje, 'tucorreo@gmail.com', [correo_destino])
