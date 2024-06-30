from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Usuario,Publicacion  # Importa tu modelo Usuario personalizado

@login_required
def listarProductosDonados(request):
    usuario = Usuario.objects.get(pk=request.user.pk) 
    publicaciones = Publicacion.objects.filter(stock__gt=0)  # Filtrar publicaciones con stock mayor a 0

    return render(request, 'canjearPuntos/listadoProductosDonados.html', {'usuario': usuario, 'publicaciones': publicaciones})
