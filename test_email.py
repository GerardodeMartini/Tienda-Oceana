import os
import sys
import django

# Add project path so django can load apps properly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from orders.models import Order

def test_send():
    order = Order.objects.last()
    if not order:
        print("ERROR: No orders found in the database. Can't render the email without an order.")
        return

    target_email = settings.ADMIN_EMAIL
    print(f"Sending test emails to: {target_email}...")

    # 1. Test Transferencia (Bank Transfer)
    order.first_name = "Gerardo"
    order.payment_method = 'transferencia'
    
    subject_transfer = f'Pedido #{order.id} registrado - Tienda Virtual (Prueba Transferencia)'
    html_transfer = render_to_string('orders/email/paid_order.html', {'order': order})
    
    try:
        send_mail(
            subject=subject_transfer,
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[target_email],
            html_message=html_transfer
        )
        print(f"SUCCESS: Transfer email test sent to {target_email}!")
    except Exception as e:
        print(f"ERROR sending Transfer email: {e}")

    # 2. Test Mercado Pago
    order.payment_method = 'mercadopago'
    
    subject_mp = f'Pedido #{order.id} confirmado - Tienda Virtual (Prueba Mercado Pago)'
    html_mp = render_to_string('orders/email/paid_order.html', {'order': order})
    
    try:
        send_mail(
            subject=subject_mp,
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[target_email],
            html_message=html_mp
        )
        print(f"SUCCESS: Mercado Pago email test sent to {target_email}!")
    except Exception as e:
        print(f"ERROR sending Mercado Pago email: {e}")

if __name__ == '__main__':
    test_send()
