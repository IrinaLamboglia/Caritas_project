
from django.shortcuts import get_object_or_404, redirect, render
from core.models import Categoria

def mostrar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'agregar_categoria/mostrarCategoria.html', {'categorias': categorias})

def bajar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, pk=categoria_id)
    if request.method == 'POST':
        print('Se ejecuta')
        categoria.delete()
        return redirect('mostarCategoria')
    return render(request, 'bajaCategoria/confirmacionBaja.html', {'categoria': categoria})

