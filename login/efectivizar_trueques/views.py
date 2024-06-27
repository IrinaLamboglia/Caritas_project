from django.shortcuts import render, redirect, get_object_or_404
from core.models import Trueque,Solicitud,Usuario,Filial,Turno
from django.db.models import Q
from django.contrib.auth import get_user_model

from django.core.mail import send_mail
from django.contrib import messages
from django.utils import timezone
import datetime
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.db.models import Q
import datetime
def efectivizar_trueques(request):
    usuario_actual = get_user_model().objects.get(pk=request.user.id)
   
    # Obtener la filial asociada al usuario actual
    filial_usuario = usuario_actual.filial_nombre
    
    # Obtener la fecha actual
    today = timezone.now().date() 

    # Inicializar trueques con una lista vacía
    trueques = []

    # Filtrar los turnos basados en la fecha y la filial del usuario
    turnos = Turno.objects.filter( filial__nombre=filial_usuario,fecha=today)

    # Verificar si se encontraron turnos para la fecha y la filial del usuario
    if turnos.exists():
        # Si se encontraron turnos, obtener el primero
        turno_actual = turnos.first()
        print(turno_actual)
        # Filtrar los Trueques basados en el turno actual y otros criterios
        query = request.GET.get('q')
        if query:
            trueques = Trueque.objects.filter(
                Q(codigo_confirmacion_solicitante=query) | Q(codigo_confirmacion_receptor=query),
                turno=turno_actual  # Filtrar por el turno actual
            )
            if not trueques.exists():
                messages.error(request, 'No se encontró ningún trueque con el código proporcionado.')
        else:
            print("entro")
            trueques = Trueque.objects.filter(turno=turno_actual, aceptado=False, confirmado=True,estado='pendiente')
    else:
        # Si no se encontraron turnos para la fecha y la filial del usuario, manejar la situación apropiadamente
        messages.error(request, 'No se encontraron turnos para la fecha y la filial especificadas.')
        

    return render(request, 'efectivizar_trueque/efectivizar_trueque.html', {'trueques': trueques})

def enviar_correo_ayudante(ayudante):
    asunto = "No olvides de calificar el producto"
    mensaje = f"¡Hola {ayudante.nombre} {ayudante.apellido}! Recuerda califica el producto una vez terminado el trueque, Saludos."
    correo_destino = ayudante.email
    send_mail(asunto, mensaje, 'tucorreo@gmail.com', [correo_destino])

def aceptacion_trueque(request, id):
    trueque = get_object_or_404(Trueque, id=id)
    trueque.aceptado = True
    trueque.estado = 'aceptado'
    trueque.fecha_efectivizacion = timezone.now().date()
    
    solicitud = Solicitud.objects.filter(trueque=id ).first()
    
    if solicitud:
        print("entro acep")
        solicitud.realizado = True
        solicitud.estado = True
        solicitud.publicacion.estado = False
        solicitud.trueque=trueque
        solicitud.save()

    trueque.save()
    enviar_correo_ayudante(trueque.solicitante)
    enviar_correo_ayudante(trueque.receptor)

    return redirect('efectivizar_trueque')




def rechazar_efectivizacion(request, id):
    try:
        trueque = Trueque.objects.get(id=id)
    except Trueque.DoesNotExist:
        messages.error(request, 'El Trueque no existe.')
        return redirect('efectivizar_trueque')
    
    solicitud = Solicitud.objects.filter(
        solicitante=trueque.solicitante,
        publicacionOfrecida__usuario=trueque.receptor,
        trueque=trueque
    ).first()
    if solicitud:
        solicitud.estado = False
        solicitud.publicacion.estado = True
        solicitud.publicacionOfrecida.estado = True
        solicitud.publicacion.save()
        solicitud.publicacionOfrecida.save()
        solicitud.delete()

    trueque.fecha_efectivizacion = timezone.now().date()
    trueque.estado = 'rechazado'
    trueque.save()

    messages.success(request, 'El trueque ha sido rechazado y las publicaciones reactivadas.')
    return redirect('efectivizar_trueque')

def penalizar_trueque(request, trueque_id):
    if request.method == 'POST':
        trueque = get_object_or_404(Trueque, id=trueque_id)
        usuario = trueque.solicitante
        usuario.puntuacion -= 1
        usuario.save()

        solicitud = Solicitud.objects.filter(
            solicitante=trueque.solicitante,
            publicacionOfrecida__usuario=trueque.receptor,
            trueque=trueque
        ).first()
        if solicitud:
            solicitud.estado = False
            solicitud.publicacion.estado = True
            solicitud.publicacionOfrecida.estado = True
            solicitud.publicacion.save()
            solicitud.publicacionOfrecida.save()
            solicitud.delete()

        trueque.fecha_efectivizacion = timezone.now().date()
        trueque.estado = 'penalizado'
        trueque.save()

        messages.success(request, 'El usuario ha sido penalizado y las publicaciones reactivadas.')

    return redirect('efectivizar_trueque')
