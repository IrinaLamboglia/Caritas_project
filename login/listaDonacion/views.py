# views.py
from django.shortcuts import render
from core.models import Donation
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import mercadopago
import logging

logger = logging.getLogger(__name__)

mp = mercadopago.SDK("APP_USR-532683645064806-061023-0dfcd038408f1614d15efd6403155a09-606424946")

def donation_list(request):
    # Filtra solo las donaciones con el estado "Aprobado"
    donations = Donation.objects.filter(status='approved')
    total_amount = donations.aggregate(total=Sum('monto'))['total'] or 0

    context = {
        'donaciones': donations,
        'total_donado': total_amount,
    }

    return render(request, 'listarDonacion/donation_list.html', context)

@csrf_exempt
def notificaciones(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f"Notificación recibida: {data}")

            # Obtener los datos relevantes de la notificación
            preference_id = data.get('data', {}).get('id')
            topic = data.get('type')
            if topic == 'payment':
                # Llamar a la API de Mercado Pago para obtener los detalles del pago
                payment_info = mp.payment().get(preference_id)
                payment_data = payment_info.get('response', {})

                if payment_data.get('status') == 'approved':
                    monto = payment_data.get('transaction_amount')
                    status = payment_data.get('status')

                    # Buscar la donación por el preference_id
                    donation, created = Donation.objects.get_or_create(
                        preference_id=preference_id,
                        defaults={'monto': monto, 'status': status, 'date': timezone.now()}
                    )

                    if not created:
                        # Si ya existe, actualizar la donación
                        donation.monto = monto
                        donation.status = status
                        donation.date = timezone.now()
                        donation.save()

                    return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'ignored'}, status=200)
        except Exception as e:
            logger.error(f"Error al procesar la notificación: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'only POST allowed'}, status=405)