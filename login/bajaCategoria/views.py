
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from core.models import Categoria

from django.contrib import messages

def bajar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    if request.method == 'POST':
        # Establecer el estado de todos los productos de esta categoría en False
        productos = categoria.productos.all()
        for producto in productos:
            producto.estado = False
            producto.categoria = None
            producto.save()
        
        # Eliminar la categoría
        categoria.delete()
        
        messages.success(request, f'Baja Exitosa.')
        return redirect('mostarCategoria')
        
    return render(request, 'bajaCategoria/confirmacionBaja.html', {'categoria': categoria})

