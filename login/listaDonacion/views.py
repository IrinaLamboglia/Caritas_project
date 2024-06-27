# views.py
from django.shortcuts import render
from core.models import Donation
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
def receive_donation(request):
    if request.method == 'POST':
        try:
            # Procesar los datos del body (JSON)
            data = json.loads(request.body)
            payment_id = data.get('data', {}).get('id')
            payment_type = data.get('type')

            if not payment_id or payment_type != 'payment':
                return JsonResponse({'error': 'Datos inválidos'}, status=400)

            # Usar SDK de Mercado Pago para obtener detalles del pago
            payment_info = mp.payment().get(payment_id)
            payment = payment_info.get('response', {})

            amount = payment.get('transaction_amount', 0.0)
            collection_status = payment.get('status', '')


            # Guardar en la base de datos
            donation = Donation.objects.create(monto=amount, status=collection_status)

            return JsonResponse({'message': 'Donación recibida correctamente', 'donation_id': donation.id}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON no válido'}, status=400)

        except KeyError as e:
            return JsonResponse({'error': f'Campo requerido faltante: {e}'}, status=400)

        except Exception as e:
            logger.error(f"Error al procesar donación: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
