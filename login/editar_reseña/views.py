from django.shortcuts import render, redirect, get_object_or_404
from core.models import Valoracion
from core.form import ValoracionForm
from django.contrib.auth.decorators import login_required

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

@login_required
def editar_valoracion(request, valoracion_id):
    valoracion = get_object_or_404(Valoracion, id=valoracion_id, usuario=request.user)
    
    if request.method == 'POST':
        form = ValoracionForm(request.POST, instance=valoracion)
        if form.is_valid():
            comentario = form.cleaned_data.get('comentario')
            if comentario:
                for palabra in PALABRAS_PROHIBIDAS:
                    if palabra in comentario.lower():
                        form.add_error('comentario', f'El comentario contiene una palabra prohibida: {palabra}')
                        return render(request, 'validar_trueque/editar_valoracion.html', {'form': form, 'valoracion': valoracion})
            form.save()
            return redirect('perfil')  # por ahora a inicio, después sería a la lista de todos los comentarios
    else:
        form = ValoracionForm(instance=valoracion)

    return render(request, 'validar_trueque/editar_valoracion.html', {'form': form, 'valoracion': valoracion})
