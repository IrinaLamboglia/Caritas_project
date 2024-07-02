# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Solicitud, Valoracion
from core.form import ValoracionForm  # Asegúrate de importar correctamente tu formulario
from django.urls import reverse

from urllib.parse import urlencode
def valorar_trueque(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)

    
    if request.method == 'POST':
        form = ValoracionForm(request.POST, solicitud=solicitud)
        if form.is_valid():
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
