from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Publicacion, BusquedaFavorita
from django.db.models import Q
import json

@login_required
def buscar_productos(request):
    query = request.GET.get('q', '')
    ya_favorita = BusquedaFavorita.objects.filter(usuario=request.user, termino_busqueda=query).exists()
    favoritas = BusquedaFavorita.objects.filter(usuario=request.user)
    
    resultados = Publicacion.objects.filter(
        Q(titulo__icontains=query) | Q(descripcion__icontains=query)
    ) if query else Publicacion.objects.all()

    if request.method == 'POST':
        if ya_favorita:
            BusquedaFavorita.objects.filter(usuario=request.user, termino_busqueda=query).delete()
            ya_favorita = False
            messages.success(request, 'Búsqueda eliminada de favoritos.')
        else:
            BusquedaFavorita.objects.create(usuario=request.user, termino_busqueda=query)
            ya_favorita = True
            messages.success(request, 'Búsqueda añadida a favoritos.')

    context = {
        'query': query,
        'resultados': resultados,
        'favoritas': favoritas,
        'ya_favorita': ya_favorita,
    }
    return render(request, 'buscarProductos/buscar_productos.html', context)

@login_required
def products(request):
    favoritas = BusquedaFavorita.objects.filter(usuario=request.user)
    publicaciones = Publicacion.objects.all()

    context = {
        'favoritas': favoritas,
        'publicaciones': publicaciones,
    }
    return render(request, 'products.html', context)