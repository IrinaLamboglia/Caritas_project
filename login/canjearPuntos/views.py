from datetime import datetime
import io
import os
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from core.models import Usuario,Publicacion, Canje 
from reportlab.lib.pagesizes import letter 
from reportlab.pdfgen import canvas  
import uuid


def generar_codigo_unico():
    return uuid.uuid4().hex[:6]


@login_required
def listarProductosDonados(request):
    usuario = Usuario.objects.get(pk=request.user.pk) 
    publicaciones = Publicacion.objects.filter(estado=True, stock__gt=0)
    message = request.session.pop('message', None)


    return render(request, 'canjearPuntos/listadoProductosDonados.html', {'usuario': usuario, 'publicaciones': publicaciones, 'message': message})


def canjear_producto(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    usuario = get_object_or_404(Usuario, id=request.user.id)  

    if usuario.puntos >= publicacion.categoria.puntuacion:
        codigo_retiro = generar_codigo_unico()

      
        print("Estoy entrando bien")
        usuario.puntos -= publicacion.categoria.puntuacion
        usuario.save()

        #publicacion.estado = False 
        publicacion.stock -= 1
        publicacion.save()

        canje = Canje.objects.create(
            usuario=usuario,
            publicacion=publicacion,
            codigo_retiro=codigo_retiro,
            estado=False  
        )
        canje.save()



        request.session['codigo_retiro'] = codigo_retiro

        enlace_descarga = request.build_absolute_uri('/generar_pdf/')
        mensaje_exito = (
            f"Canje exitoso para '{publicacion.titulo}'. Código de retiro: {codigo_retiro}. "
            f"<a href='{enlace_descarga}?codigo_retiro={codigo_retiro}' class='btn btn-success' style='margin-left: 10px;'>Descargar comprobante</a>"
        )
        request.session['message'] = {'content': mensaje_exito, 'type': 'success'}
    else:
        request.session['message'] = {'content': "Solicitud inválida: No tienes suficientes puntos para canjear este producto.", 'type': 'error'}
    
    return redirect('listadoProductosDonados')


# ya funciona :)
def generar_pdf(request):
    codigo_retiro = request.session.get('codigo_retiro', None)
    if not codigo_retiro:
        messages.error(request, "No hay código de retiro disponible.")
        return redirect('listadoProductosDonados')

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    current_dir = os.path.dirname(__file__)
    logo_path = os.path.join(current_dir, 'logoCaritas.jpg')
    if os.path.exists(logo_path):
        try:
            p.drawImage(logo_path, 200, 600, width=200, height=100)
        except Exception as e:
            print(f"Error loading logo image: {e}")
    else:
        print(f"Logo path not found: {logo_path}")

    p.drawString(100, 500, f"Código de retiro: {codigo_retiro}")
    fecha_transaccion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    p.drawString(100, 480, f"Fecha de transacción: {fecha_transaccion}")
    p.drawString(100, 460, "Gracias por tu canje.")
    
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'imagenes', 'logoCaritas.jpg')
    
    if os.path.exists(logo_path):
        try:
            p.drawImage(logo_path, 100, 700, width=300, height=100)
        except Exception as e:
            print(f"Error loading logo image: {e}")
    else:
        print(f"Logo path not found: {logo_path}")
        
    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="comprobante.pdf"'
    return response


def misCanjes(request):
    usuario = get_object_or_404(Usuario, id=request.user.id)  

    canjes = Canje.objects.filter(usuario=usuario)
    return render(request, 'canjearPuntos/misCanjes.html', {'usuario': usuario, 'canjes': canjes})
