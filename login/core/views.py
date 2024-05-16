from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import FailedLoginAttempt, Publicacion, Usuario, UsuarioBloqueado, porDesbloquear, Categoria
from django.contrib.auth import login
from . formreg import UsuarioForm
import logging
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.conf import settings
import random
from django.core.mail import send_mail
import string
from .globals import contenido_actual
from .formpubl import PublicacionForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

#los css los restaure por las dudas por si llega a haber conflicto
#estan al pedo, en deshuso
#solo hay que mantener estilo.css y login-estilos.css






#con esto estoy diciendo que me tengo que loguear para acceder
#a una vista 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


# Create your views here.
logger = logging.getLogger(__name__)





def home(request):
    #Publicacion.objects.all().delete()
    #Categoria.objects.all().delete()
    user = request.user  # Obtiene el usuario autenticado de la sesión
    context = {
        'user': user,
        'contenido_actual': contenido_actual,  # Agrega la variable global contenido_actual al contexto
    }
    return render(request, 'home.html', context)

#estoy aplicando la restrinccion de que si no esta logueado
#no puude ver los productos
#el template login es lo que se muestra antes de q se loguee
@login_required
def products(request):
    publicaciones = Publicacion.objects.filter(estado=True)
    return render(request, 'core/products.html',{'publicaciones': publicaciones})

#funcion para salir
##def exit(request):
##    logout(request)
##    print("saliendo")
##    return redirect('home')




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
                     user=UsuarioBloqueado.objects.get(email=email) #esta bloqueado
                     print(user.email)
                     error_message = 'El Usuario esta bloqueado'
                     #aca lo redirige para mostrarle el mensaje y habilitarle el boton


                     return render(request, 'login.html', {'error_message': error_message , 'user' : user})
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
                 try:
                     user= UsuarioBloqueado.objects.get(email=email)  #contraseña incorrecta y esta bloqueado
                     print(user.email)
                     error_message = 'El Usuario esta bloqueado'
                     #aca lo redirige para mostrarle el mensaje y habilitarle el boton

                     return render(request, 'login.html', {'error_message': error_message , 'user' : user})
                 except UsuarioBloqueado.DoesNotExist: #contra inco no bloqueado
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

def enviar_correo_ayudante(ayudante):
    asunto = "Bienvenido a nuestra plataforma"
    mensaje = f"¡Hola {ayudante.nombre} {ayudante.apellido}! Te hemos registrado en nuestra plataforma como ayudante. Te enviamos tu informacion para que puedas iniciar sesion: Nombre de usuario: {ayudante.email} y la contraseña:{ayudante.contraseña}. Saludos."
    correo_destino = ayudante.email
    send_mail(asunto, mensaje, 'tucorreo@gmail.com', [correo_destino])

#perfecto
def formularioreg(request):
    print("Ejecutando recibo de registro")
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            print("El formulario es válido")
            usuario = form.save()
            
            
            if (request.user.is_authenticated):
                if (request.user.tipo == "administrador"):
                     usuario.email = usuario.email  # Establecer el nombre de usuario como el correo electrónico
                     usuario.tipo="ayudante"
                     usuario.save()
                     enviar_correo_ayudante(request.user)
                     return redirect('home')
            form.save()
            return redirect('login')
    else:
        print("El formulario es inválido")
        form = UsuarioForm()

    return render(request, 'registration/registro.html', {'form': form})

#perfecto
def mostrarBaja(request):
     email = request.POST.get('text') #tomo el texto(email) de la persona q quiere bajar
     if(email == None): #no ingreso ningun text
         sin="no"
         return render(request, 'core/bajaAyudante/bajaAyudante.html', {'sin': sin})
     try:
         elementos = Usuario.objects.get(email=email) #si esta en el try ingreso texto
         if(elementos.tipo == "ayudante"):
             return render(request, 'core/bajaAyudante/bajaAyudante.html', {'elementos': elementos}) #le paso el q quiere bajar solo si es ayudate(pudo haber puesto el mail de un usu normal            
         else:
             return render(request, 'core/bajaAyudante/bajaAyudante.html') #ayudante no existe
     except Usuario.DoesNotExist:
         return render(request, 'core/bajaAyudante/bajaAyudante.html')#ayudante no existe

#anda bien, chequear si lo tengo que bajr de otro modelo(chicas)
def eliminarAyudante(request,email):
     Usuario.objects.filter(email=email).delete()
     return render(request, 'core/bajaAyudante/bajaAyudante.html', {'error_message': 'Se ha eliminado con exito'})


#anda bien, chequear si lo tengo que bajr de otro modelo(chicas)
def eliminarAyudante(request,email):
     Usuario.objects.filter(email=email).delete()
     return render(request, 'core/bajaAyudante/bajaAyudante.html', {'error_message': 'Se ha eliminado con exito'})

def recuperarCuenta(request,email):
     print("estoy en la funcion recuperar cuenta")
     try:
         porDesbloquear.objects.get(email=email)  #si existe no lo guardo
     except porDesbloquear.DoesNotExist:
         print("estoy por guardarlo en por desbloquear")
         porDesbloquear.objects.create(email=email)    #lo agrego a usuarios bloqueados
     return render(request,'login.html', {'error_message': 'Se ha registrado su peticion con exito'})
    

#perfecto
def listadoBloqueado(request):
    #para probar
    #email="g@gmail.com"
    #porDesbloquear.objects.create(email=email) 
    #email="yo@gmail.com"
    #porDesbloquear.objects.create(email=email) 
    elementos = porDesbloquear.objects.all()
    return render(request, 'core/listado/bloqueadosListado.html', {'elementos': elementos})

def editar_sobre_nosotros(request):
    global contenido_actual
    if request.method == 'POST':
        nuevo_contenido = request.POST.get('nuevo_contenido')
        contenido_actual = nuevo_contenido
        return redirect('home')
    else:
        return render(request, 'core/editar_sobre_nosotros.html', {'contenido_actual': contenido_actual})


@login_required
def crear_publicacion(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        formulario = PublicacionForm(request.POST, request.FILES)
        if formulario.is_valid():
            publicacion = formulario.save(commit=False)
            publicacion.usuario = request.user
            publicacion.estado = False;
            publicacion.save()
            messages.success(request,'La publicación se registró correctamente, queda a la espera de validación')
            return redirect('products')
        else:
            messages.error(request, 'Hubo un problema al cargar la publicación')
    else:
          formulario = PublicacionForm()
    return render(request, 'core/crearPublicacion/crear_publicacion.html', {'categorias': categorias,'formulario': formulario}) 


def ver_producto(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    return render(request, 'core/crearPublicacion/ver_producto.html', {'publicacion': publicacion})

def solicitar_trueque(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    return render(request, 'core/crearPublicacion/solicitar_trueque.html',  {'publicacion': publicacion})


def desbloquearUsuario(request, email):
    user = Usuario.objects.get(email=email)
    nueva_contraseña = ''.join(random.choices(string.ascii_letters + string.digits, k=max(6, 10)))

    user.contraseña = nueva_contraseña
    user.save()

    send_mail(
        'Contraseña restablecida',
        f'Su nueva contraseña es: {nueva_contraseña}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

    # Eliminar al usuario de las tablas porDesbloquear y usuarioBloqueado
    porDesbloquear.objects.filter(email=email).delete()
    UsuarioBloqueado.objects.filter(email=email).delete()

    # Restablecer los intentos fallidos a 0
    FailedLoginAttempt.objects.filter(email=email).delete()
   


    return redirect('listadoBloqueados')

def mis_publicaciones(request):
    publicaciones = Publicacion.objects.filter(usuario=request.user)
    return render(request, 'core/crearPublicacion/mis_publicaciones.html', {'publicaciones': publicaciones})

@csrf_exempt
def eliminar_publicacion(request, publicacion_id):
    print("fuera del try")
    if request.method == 'DELETE':
        try:
            print("entra al try")
            publicacion = Publicacion.objects.get(pk=publicacion_id)
            publicacion.delete()
            mensaje = 'La publicación ha sido eliminada correctamente.'
            return JsonResponse({'message': mensaje}, status=200)
        except Publicacion.DoesNotExist:
            mensaje = 'La publicación no existe.'
            return JsonResponse({'error': mensaje}, status=404)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)