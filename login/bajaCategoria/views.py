
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from core.models import Categoria, Publicacion

from django.contrib import messages

def bajar_categoria(request, categoria_id):
    print(categoria_id)
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    if request.method == 'POST':
        # Establecer el estado de todos los publicacions de esta categoría en False
        publicaciones = Publicacion.objects.filter(categoria = categoria_id)
        for publicacion in publicaciones:
            publicacion.estado = False
            publicacion.categoria = None
            publicacion.save()
        
        # Eliminar la categoría
        categoria.delete()
        
        messages.success(request, f'Baja Exitosa.')
        return redirect('mostarCategoria')
        
    return render(request, 'bajaCategoria/confirmacionBaja.html', {'categoria': categoria})

