from django.shortcuts import render
from django.http import JsonResponse
import mercadopago
from django.urls import reverse

mp = mercadopago.SDK("APP_USR-532683645064806-061023-0dfcd038408f1614d15efd6403155a09-606424946")

def realizar_donacion(request):
    if request.method == 'POST':
        nombre_usuario = request.POST.get('nombre_usuario', 'Anónimo')
        monto = request.POST.get('monto')

        # Crear preferencia de Mercado Pago
        preference_data = {
            "items": [
                {
                    "title": "Donación",
                    "quantity": 1,
                    "unit_price": float(monto)
                }
            ],
            "payer": {
                "name": nombre_usuario if nombre_usuario else "Anónimo"
            },
            "back_urls": {
                "success": request.build_absolute_uri(reverse('home')),
                "failure": request.build_absolute_uri(reverse('home')),
                "pending": request.build_absolute_uri(reverse('home'))
            },
            "auto_return": "approved",
        }

        try:
            preference_response = mp.preference().create(preference_data)
            init_point = preference_response["response"]["init_point"]
            qr_code = generate_qr_code(init_point)

            return JsonResponse({
                'init_point': init_point,
                'qr_code': qr_code
            })
        except Exception as e:
            print(f"Error al crear la preferencia de Mercado Pago: {e}")
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'realizarDonacion/realizar_donacion.html')

def generate_qr_code(url):
    import qrcode
    import base64
    from io import BytesIO

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return img_str
