from django.shortcuts import render, redirect
from .models import FailedLoginAttempt, Usuario, UsuarioBloqueado
from django.contrib.auth import login, logout
from . formreg import UsuarioForm
import logging
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import os
from django.conf import settings
import random
import string
#con esto estoy diciendo que me tengo que loguear para acceder
#a una vista 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# Create your views here.
logger = logging.getLogger(__name__)





def home(request):
    user = request.user  # Obtiene el usuario autenticado de la sesión
    context = {'user': user}
    return render(request, 'home.html', context)


#estoy aplicando la restrinccion de que si no esta logueado
#no puude ver los productos
#el template login es lo que se muestra antes de q se loguee
@login_required
def products(request):
    return render(request, 'core/products.html')

#funcion para salir
def exit(request):
    logout(request)
    print("saliendo")
    return redirect('home')




def generar_codigo_aleatorio(longitud):
    caracteres = string.ascii_letters + string.digits
    codigo = ''.join(random.choice(caracteres) for _ in range(longitud))
    return codigo


#perfecto
def login_nuevo(request):
    error_message = None
    failed_attempts = None

    if request.method == 'POST':
        # Tomar los datos del formulario
        email = request.POST.get('email')  
        contraseña = request.POST.get('contraseña') 
        print(contraseña)
        #UsuarioBloqueado.objects.filter(email=email).delete()
        #FailedLoginAttempt.objects.filter(email=email).delete()

        try:
            usuario = Usuario.objects.get(email=email)  # Intenta encontrar el usuario por su email, si se queda en el try existe
            if contraseña == usuario.contraseña: #autenticacion exitosa
                try:
                     UsuarioBloqueado.objects.get(email=email) #esta bloqueado
                     error_message = 'El Usuario esta bloqueado'
                     return render(request, 'login.html', {'error_message': error_message})
                except UsuarioBloqueado.DoesNotExist:         #autenticacion exitosa y usuario no bloqueado
                     if(usuario.tipo=="ayudante"):
                         #hago una clave aleatorea, se la envio por mail
                         #lo redirijo a un segundo formulario para que se loguee
                         codigo = generar_codigo_aleatorio(6)
                         request.session['codigo_autenticacion'] = codigo #guardo temporalmente la clave en la sesion 
                         subject = 'Codigo autenticacion' 
                         template = render_to_string('correos\email_template.html', {
                             'name' : usuario.nombre ,
                             'email' : usuario.email ,
                             'message' : f"Codigo aleatoreo de autenticacion {codigo}"
                         })
                         email = EmailMessage(
                             subject,
                             template,
                             settings.EMAIL_HOST_USER,
                             [usuario.email]
                         )
                         email.fail_silently = False 
                         email.send()
                         request.session['_auth_user_id'] = usuario.id   #me guardo el usuario
                         return render(request, 'login_ayudante.html', {'messages': 'Se ha enviado el codigo de autenticacion a su correo'})
                     login(request, usuario)
                     print("estoy con los datos correctos")
                # Elimina los intentos fallidos anteriores (si los hay)
                     FailedLoginAttempt.objects.filter(email=email).delete()
                # Redirige al usuario a la página de inicio
                     print(usuario.email)
                     print(usuario.contraseña)
                     return redirect('home')
            else:
                 print("La autenticación falló debido a la contraseña incorrecta")
                 print(usuario.contraseña)
                # Registra el intento fallido en la base de datos
                 FailedLoginAttempt.objects.create(email=email)
                # Contabiliza el número de intentos fallidos para este usuario
                 failed_attempts = FailedLoginAttempt.objects.filter(email=email).count()
                # Si el número de intentos fallidos es igual a 3, bloquea la cuenta
                 if failed_attempts == 3:
                    # Se bloquea el usuario y se le manda mail de recuperacion
                     UsuarioBloqueado.objects.create(email=email)    #lo agrego a usuarios bloqueados
                    #  dijimos q no ibamos a enviar correos enviar_correo(usuario.email, 'Cuenta bloqueada', 'Su cuenta ha sido bloqueada debido a múltiples intentos de inicio de sesión fallidos.Para recuperarla ingrese al siguiente link : ')
                     return render(request, 'login.html', {'error_message': 'Cuenta bloqueada: Supero los intentos fallidos permitidos'})
                 else:
                     error_message = f'Contraseña incorrecta, cantidad de intentos fallidos: {failed_attempts}'
        except Usuario.DoesNotExist:
            # Si el usuario no existe en la base de datos, la autenticación falló debido al nombre de usuario incorrecto
            error_message = 'El nombre de usuario no existe'
            print("Error:", error_message)  # Imprime el mensaje de error en la consola
            print("Failed attempts:", failed_attempts)  # Imprime el número de intentos fallidos en la consola
    # Si no es una solicitud POST o si la autenticación falló, renderizar el formulario de inicio de sesión nuevamente
    return render(request, 'login.html', {'error_message': error_message})




#perfecto
def procesar_clave(request):
    if request.method == 'POST':
        clave_ingresada = request.POST.get('clave')
        codigo_correcto = request.session.get('codigo_autenticacion')

        if clave_ingresada == codigo_correcto:
            usuario_id = request.session.get('_auth_user_id')
            if usuario_id is not None:
                print("recupere el usuario")
                usuario = Usuario.objects.get(id=usuario_id)
                print(usuario.email)
                request.session.pop('codigo_autenticacion', None)
                login(request, usuario)
                return redirect('home')
        else:
            messages = "Clave incorrecta: por favor intentelo de nuevo"
    # Si no es una solicitud POST o la clave es incorrecta, redirige a la página de inicio de sesión.
   # return redirect('login_ayudante')
    return render(request, 'login_ayudante.html', {'messages': messages})



#perfecto
def formularioreg(request):
    print("ejecutando recibo de regisro")
    if request.method =='POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            print("el formulario es valido")
            form.save()
            return redirect('login')
    else:
        print("el formulario es invalido")
        form = UsuarioForm()  

    return render(request, 'registration/registro.html', {'form': form}) 

def mostrarBaja(request):
     print("estoy aca")
     elementos = Usuario.objects.all()
     return render(request, 'core/bajaAyudante/bajaAyudante.html', {'elementos': elementos})









