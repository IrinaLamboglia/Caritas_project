from django.shortcuts import render, redirect
from .models import FailedLoginAttempt, Usuario, UsuarioBloqueado
from django.contrib.auth import authenticate, login, logout
from . formreg import UsuarioForm
from django.core.mail import send_mail
import logging
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail import send_mail
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail




#con esto estoy diciendo que me tengo que loguear para acceder
#a una vista 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# Create your views here.
logger = logging.getLogger(__name__)



def home(request):
    print("HOLA")
    print(request.session.get('user_email'))
    user = Usuario.objects.get(email=request.session.get('user_email')) 
    #user = request
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





def enviar_correo(usuario_email, asunto, mensaje):
    try:
        # Configura el cliente de SendGrid con tu API Key
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

        # Crea el objeto Mail con los detalles del correo electrónico
        message = Mail(
            from_email='giuproyectocaritas@gmail.com',
            to_emails=usuario_email,
            subject=asunto,
            plain_text_content=mensaje
        )

        # Envía el correo electrónico utilizando la API de SendGrid
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)

    except Exception as e:
        # Manejo de errores
        print(f"Error al enviar correo electrónico: {str(e)}")



#andas
#no puedo usar authenticate porque estoy usando otro modelo de bd 
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
                     error_message = 'El Usuario esta bloqueado, para desbloquearlo debe enviar un mail a la fundacion'
                     return render(request, 'login.html', {'error_message': error_message})
                except UsuarioBloqueado.DoesNotExist:         #autenticacion exitosa y usuario no bloqueado
                     login(request, usuario)
                     print("estoy con los datos correctos")
                # Elimina los intentos fallidos anteriores (si los hay)
                     FailedLoginAttempt.objects.filter(email=email).delete()
                # Redirige al usuario a la página de inicio
                     print(usuario.email)
                     print(usuario.contraseña)
                     request.session['user_email'] = usuario.email
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
                     enviar_correo(usuario.email, 'Cuenta bloqueada', 'Su cuenta ha sido bloqueada debido a múltiples intentos de inicio de sesión fallidos.Para recuperarla ingrese al siguiente link : ')
                     return render(request, 'login.html', {'error_message': 'Cuenta bloqueada: Para desbloquear la cuenta comuníquese vía mail con la fundación'})
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






