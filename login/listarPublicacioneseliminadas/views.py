from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Publicacion

@login_required
def listar_publicaciones_eliminadas(request):
    publicaciones_eliminadas = Publicacion.objects.filter(usuario=request.user, eliminada=True)
    return render(request, 'core/crearPublicacion/listar_eliminados.html', {'publicaciones': publicaciones_eliminadas})
