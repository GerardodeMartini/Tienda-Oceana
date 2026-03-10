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
    order = Order.objects.filter(payment_method='transferencia').last()
    if not order:
        order = Order.objects.last()

    if order:
        # Override fields just for the email appearance
        order.first_name = "Gerardo"
        order.payment_method = 'transferencia'
        
        subject = f'Pedido #{order.id} confirmado - Diseño Prueba'
        html_message = render_to_string('orders/email/paid_order.html', {'order': order})
        target_email = 'gerardodemartini@gmail.com'
        
        try:
            send_mail(
                subject=subject,
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[target_email],
                html_message=html_message
            )
            print(f"SUCCESS: Email test successfully sent to {target_email}!")
        except Exception as e:
            print(f"ERROR: Error sending email: {e}")
    else:
        print("ERROR: No orders found in the database. Can't render the email without an order.")

if __name__ == '__main__':
    test_send()
