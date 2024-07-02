# core/views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Solicitud, Valoracion
from core.form import ValoracionForm  # Asegúrate de importar correctamente tu formulario
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from urllib.parse import urlencode
#creo la lista de palabras prohibidas 
PALABRAS_PROHIBIDAS = [
    'estafa', 'fraude', 'engaño', 'mentira', 'basura', 'mierda', 'puto', 
    'puta', 'imbecil', 'idiota', 'tonto', 'estúpido', 'pendejo', 'maldito', 
    'maldita', 'asqueroso', 'asco', 'decepcionante', 'inutil', 'horrible', 
    'malo', 'peor', 'desastroso', 'tragedia', 'vergonzoso', 'ridículo', 
    'bobo', 'burro', 'cabrón', 'cabrona', 'carajo', 'coño', 'culo', 'estupidez',
    'gilipollas', 'jodido', 'joder', 'lameculo', 'mamón', 'mierdero', 
    'nefasto', 'patético', 'pelotudo', 'perra', 'picha', 'pito', 'puta madre', 
    'putada', 'tarado', 'vergüenza'
]
#funcion que lo chequea 
def validar_palabras_prohibidas(comentario):
    for palabra in PALABRAS_PROHIBIDAS:
        if palabra.lower() in comentario.lower():
            return False
    return True

def valorar_trueque(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)

    
    if request.method == 'POST':
        form = ValoracionForm(request.POST, solicitud=solicitud)
        if form.is_valid():
            comentario = form.cleaned_data.get('comentario')
            if not validar_palabras_prohibidas(comentario):
                form.add_error('comentario', 'Tu comentario contiene palabras prohibidas. Por favor, revísalo.')
            else:
                valoracion = form.save(commit=False)
                valoracion.trueque = solicitud.trueque
                valoracion.solicitud = solicitud
                valoracion.usuario = request.user
                valoracion.save()
                # Construir la URL con el filtro "Pendientes en valoración"
                base_url = reverse('filtro_trueques')
                query_string = urlencode({'filtro': 'Pendientes en valoración'})
                url = f'{base_url}?{query_string}'
                return redirect(url) 
        else:
            form = ValoracionForm( solicitud=solicitud)

    return render(request, 'validar_trueque/validar.html', {'form': form, 'solicitud': solicitud})

@csrf_exempt
def eliminar_valoracion(request, valoracion_id):
    if request.method == 'DELETE':
        valoracion = get_object_or_404(Valoracion, id=valoracion_id)
        valoracion.delete()
        return JsonResponse({'success': True, 'message': 'Se ha eliminado la valoración exitosamente.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)