from django.shortcuts import render
from core.models import Trueque, Categoria, Publicacion, Usuario
from datetime import datetime
from django.http import JsonResponse, HttpResponseServerError
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist

def estadisticas_trueques(request):
    try:
        # Obtener la fecha seleccionada para estadísticas de trueques
        fecha_trueques_str = request.GET.get('fecha_trueques', datetime.now().date().strftime('%Y-%m-%d'))
        fecha_trueques = datetime.strptime(fecha_trueques_str, '%Y-%m-%d').date()

        # Filtrar trueques para la fecha seleccionada y agrupar por estado
        print(fecha_trueques)
        trueques = Trueque.objects.filter(fecha_efectivizacion=fecha_trueques) #trueques totales en esa fecha 
        
        total_trueques = trueques.count() #total(cant) de la fecha 
        trueques_aceptados = trueques.filter(estado='aceptado').count()
        trueques_rechazados = trueques.filter(estado='rechazado').count()
        trueques_penalizados = trueques.filter(estado='penalizado').count()

        # Calcular porcentajes
        if total_trueques > 0:
            porcentaje_aceptados = (trueques_aceptados / total_trueques) * 100
            porcentaje_rechazados = (trueques_rechazados / total_trueques) * 100
            porcentaje_penalizados = (trueques_penalizados / total_trueques) * 100
        else:
            porcentaje_aceptados = 0
            porcentaje_rechazados = 0
            porcentaje_penalizados = 0
        
        # Obtener todas las categorías
        categorias = Categoria.objects.all()

        # Obtener el ID de la categoría seleccionada, si está presente en la solicitud GET
        categoria_id = request.GET.get('categoria')
        publicaciones_categoria = None
        publicaciones_total = Publicacion.objects.all().count()

        # Variables para las estadísticas de la categoría seleccionada
        publicaciones_categoria_count = 0
        porcentaje_publicaciones_categoria = 0.0

        if categoria_id:
            try:
                # Obtener la categoría seleccionada
                categoria_seleccionada = Categoria.objects.get(id=categoria_id)
                # Filtrar las publicaciones por la categoría seleccionada
                publicaciones_categoria = Publicacion.objects.filter(categoria=categoria_seleccionada)
                # Obtener el número de publicaciones en esa categoría
                publicaciones_categoria_count = publicaciones_categoria.count()
                # Calcular el porcentaje de publicaciones en esa categoría
                if publicaciones_total > 0:
                    porcentaje_publicaciones_categoria = (publicaciones_categoria_count / publicaciones_total) * 100
            except ObjectDoesNotExist:
                categoria_seleccionada = None
        else:
            categoria_seleccionada = None
            # Si no se selecciona ninguna categoría, calcular el porcentaje para todas las publicaciones

        # Estadísticas de usuarios
        fecha_usuarios_str = request.GET.get('fecha_usuarios', datetime.now().date().strftime('%Y-%m-%d'))
        fecha_usuarios = datetime.strptime(fecha_usuarios_str, '%Y-%m-%d').date()
        
        #usuarios reg en la fecha seleccionada
        total_usuarios_registrados = Usuario.objects.filter(fecha__date=fecha_usuarios).exclude(tipo__in=['administrador', 'ayudante']).count()
        print(total_usuarios_registrados)
        print(fecha_usuarios)

        #total de usus normales 
        total_usuarios = Usuario.objects.exclude(tipo__in=['administrador', 'ayudante']).count()
        

        if total_usuarios > 0:
            #el porcentaje de usus en la fecha solicitada
            porcentaje_usuarios_registrados = (total_usuarios_registrados / total_usuarios) * 100
        else:
            porcentaje_usuarios_registrados = 0

        context = {
            'fecha_seleccionada_trueques': fecha_trueques_str,
            'trueques_aceptados': trueques_aceptados,
            'trueques_rechazados': trueques_rechazados,
            'trueques_penalizados': trueques_penalizados,

            'porcentaje_aceptados': porcentaje_aceptados,
            'porcentaje_rechazados': porcentaje_rechazados,
            'porcentaje_penalizados': porcentaje_penalizados,
            'total_trueques': total_trueques,

            'categorias': categorias,
            'categoria_seleccionada': categoria_seleccionada,
            'publicaciones_categoria': publicaciones_categoria,
            'publicaciones_categoria_count': publicaciones_categoria_count,
            'porcentaje_publicaciones_categoria': porcentaje_publicaciones_categoria,
            'total_usuarios_registrados': total_usuarios, #total general
            'porcentaje_usuarios_registrados': porcentaje_usuarios_registrados, #el porcentaje del dia seleccionado
            'fecha_seleccionada_usuarios': fecha_usuarios_str,
            'total_publicaciones': publicaciones_total,
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'html': render_to_string('visualizar_estadisticas/estadisticas.html', context)})

        return render(request, 'visualizar_estadisticas/estadisticas.html', context)

    except Exception as e:
        # Captura cualquier excepción para facilitar la depuración
        return HttpResponseServerError(f"Error en estadisticas_trueques: {str(e)}")
