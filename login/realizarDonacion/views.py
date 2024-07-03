from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import mercadopago
from django.urls import reverse
import logging
from django.utils import timezone
from core.models import Donation

mp = mercadopago.SDK("APP_USR-532683645064806-061023-0dfcd038408f1614d15efd6403155a09-606424946")

logger = logging.getLogger(__name__)

def realizar_donacion(request):
    status = request.GET.get('status')
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario', 'Anónimo')
        monto = float(request.POST.get('monto', 0))

        preference = {
            "items": [
                {
                    "title": f"Donación de {nombre_usuario}",
                    "quantity": 1,
                    "currency_id": "ARS",
                    "unit_price": monto
                }
            ],
            "back_urls": {
                "success": request.build_absolute_uri(reverse('donacion_success')),
                "failure": request.build_absolute_uri(reverse('donacion_failure')),
                "pending": request.build_absolute_uri(reverse('donacion_pending'))
            },
            "auto_return": "approved"
        }

        try:
            preference_result = mp.preference().create(preference)
            init_point = preference_result['response']['init_point']
            preference_id = preference_result['response']['id']

            return JsonResponse({'init_point': init_point, 'preference_id': preference_id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return render(request, 'realizarDonacion/realizar_donacion.html', {'status': status})


def donacion_success(request):
    payment_id = request.GET.get('payment_id')
    if payment_id:
        try:
            payment_info = mp.payment().get(payment_id)
            logger.info(f"Payment info response: {payment_info}")

            if 'response' in payment_info:
                payment_status = payment_info['response']['status']
                monto = payment_info['response']['transaction_amount']
                preference_id = payment_info['response']['order']['id']

                if payment_status == 'approved':
                    Donation.objects.create(monto=monto, status='approved', preference_id=preference_id, date=timezone.now())
                    return redirect(reverse('realizar_donacion') + '?status=success')
                else:
                    logger.error(f"Estado del pago no es 'approved': {payment_status}")
                    return redirect(reverse('realizar_donacion') + '?status=failure')
            else:
                logger.error(f"Respuesta no encontrada en la información del pago de Mercado Pago: {payment_info}")
                return redirect(reverse('realizar_donacion') + '?status=failure')
        except Exception as e:
            logger.error(f"Error al procesar la donación exitosa: {e}")
            return redirect(reverse('realizar_donacion') + '?status=failure')
    return redirect(reverse('realizar_donacion') + '?status=failure')

def donacion_failure(request):
    return redirect(reverse('realizar_donacion') + '?status=failure')

def donacion_pending(request):
    return redirect(reverse('realizar_donacion') + '?status=pending')

