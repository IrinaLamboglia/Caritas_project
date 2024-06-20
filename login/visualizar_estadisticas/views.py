from django.shortcuts import render
from core.models import Trueque, Categoria, Publicacion, Usuario
from datetime import datetime
from django.http import JsonResponse
from django.template.loader import render_to_string

def estadisticas_trueques(request):
    # Obtener la fecha seleccionada para estadísticas de trueques
    if 'fecha_trueques' in request.GET:
        fecha_trueques_str = request.GET.get('fecha_trueques')
        fecha_trueques = datetime.strptime(fecha_trueques_str, '%Y-%m-%d').date()
    else:
        fecha_trueques = datetime.now().date()
        fecha_trueques_str = fecha_trueques.strftime('%Y-%m-%d')
    # Filtrar trueques para la fecha seleccionada y agrupar por estado
    total_trueques = Trueque.objects.filter(fecha_efectivizacion__date=fecha_trueques).count()
    trueques_aceptados = Trueque.objects.filter(estado='aceptado', fecha_efectivizacion__date=fecha_trueques).count()
    trueques_rechazados = Trueque.objects.filter(estado='rechazado', fecha_efectivizacion__date=fecha_trueques).count()
    trueques_penalizados = Trueque.objects.filter(estado='penalizado', fecha_efectivizacion__date=fecha_trueques).count()
    
    #saco el total de trueques que tenemos 
    trueques_aceptados = Trueque.objects.filter(estado='aceptado').count()
    trueques_penalizados = Trueque.objects.filter(estado='penalizado').count()
    trueques_rechazados = Trueque.objects.filter(estado='rechazado').count()

    total = trueques_aceptados + trueques_penalizados + trueques_rechazados

    
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
        except Categoria.DoesNotExist:
            categoria_seleccionada = None
    else:
        categoria_seleccionada = None
        # Si no se selecciona ninguna categoría, calcular el porcentaje para todas las publicaciones

    # Estadísticas de usuarios
    fecha_usuarios_str = ''
    if 'fecha_usuarios' in request.GET:
        fecha_usuarios_str = request.GET.get('fecha_usuarios')
        fecha_usuarios = datetime.strptime(fecha_usuarios_str, '%Y-%m-%d').date()
    else:
        fecha_usuarios = datetime.now().date()
        fecha_usuarios_str = fecha_usuarios.strftime('%Y-%m-%d')
    total_usuarios_registrados = Usuario.objects.filter(fecha__date=fecha_usuarios).exclude(tipo__in=['administrador', 'ayudante']).count()
    total_usuarios = Usuario.objects.exclude(tipo__in=['administrador', 'ayudante']).count()
    if total_usuarios > 0:
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
        'total_trueques': total,
        'categorias': categorias,
        'categoria_seleccionada': categoria_seleccionada,
        'publicaciones_categoria': publicaciones_categoria,
        'publicaciones_categoria_count': publicaciones_categoria_count,
        'porcentaje_publicaciones_categoria': porcentaje_publicaciones_categoria,
        'categoria_seleccionada': categoria_seleccionada,
        'total_usuarios_registrados': total_usuarios,
        'porcentaje_usuarios_registrados': porcentaje_usuarios_registrados,
        'fecha_seleccionada_usuarios': fecha_usuarios_str,
        'total_publicaciones': publicaciones_total,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'html': render_to_string('visualizar_estadisticas/estadisticas.html', context)})

    return render(request, 'visualizar_estadisticas/estadisticas.html', context)
