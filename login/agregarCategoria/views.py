# views.py
from django.shortcuts import render, redirect
from core.models import Categoria

def agregar_categoria(request):
    error_message = None
    exito_message = "Categoria agreda exitosamente"
    if request.method == 'POST':
        nombre_categoria = request.POST.get('nombre_categoria')
        if not Categoria.objects.filter(nombre=nombre_categoria).exists():
            categoria = Categoria.objects.create(nombre=nombre_categoria)
            # Actualizar la lista de productos (a implementar)
            return  render(request, 'agregar_categoria/aceptarCategoria.html', {'exito_message': exito_message})  # Redirigir a la página de inicio o a donde sea necesario
        else:
            error_message = "La categoría ya está registrada"
    return render(request, 'agregar_categoria/aceptarCategoria.html', {'error_message': error_message})

def mostrar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'agregar_categoria/mostrarCategoria.html', {'categorias': categorias})