import mercadopago
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart

from cart.shipping import get_shipping_cost

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            
            # Calcular costo de envío
            shipping_price = get_shipping_cost(order.stat_province, cart.get_total_price())
            order.shipping_cost = shipping_price
            order.save()
            
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect('orders:payment_process')
    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
    
    items = []
    for item in order.items.all():
        items.append({
            "title": item.product.title,
            "quantity": item.quantity,
            "unit_price": float(item.price),
        })
    
    # Agregar Ítem de Envío si existe costo
    if order.shipping_cost > 0:
        items.append({
            "title": "Costo de Envío",
            "quantity": 1,
            "unit_price": float(order.shipping_cost),
        })
        
    success_url = request.build_absolute_uri(reverse('orders:payment_done'))
    failure_url = request.build_absolute_uri(reverse('orders:payment_canceled'))
    pending_url = request.build_absolute_uri(reverse('orders:payment_done'))

    preference_data = {
        "items": items,
        "back_urls": {
            "success": success_url,
            "failure": failure_url,
            "pending": pending_url,
        },
        # "auto_return": "approved",
        "external_reference": str(order.id),
    }
    
    # DEBUG: Print data being sent to MP
    # print("DEBUG MP Preference Data:")
    # print(preference_data)
    
    preference_response = sdk.preference().create(preference_data)
    
    # Debugging: check if the response was successful
    if preference_response["status"] >= 400:
        # Log the error for the developer
        print(f"DEBUG MP Error: {preference_response['response']}")
        # For now, let's redirect to a failure page or show an error
        return render(request, 'orders/payment/error.html', {
            'error': preference_response['response']
        })

    preference = preference_response["response"]
    
    # Check if 'id' exists in the response
    if 'id' not in preference:
        print(f"DEBUG MP Missing ID: {preference}")
        return render(request, 'orders/payment/error.html', {
            'error': 'No se pudo generar el ID de preferencia de Mercado Pago.'
        })

    # Save the MP ID to the order
    order.mercadopago_id = preference['id']
    order.save()
    
    return render(request, 'orders/payment/process.html', {
        'order': order,
        'preference_id': preference['id'],
        'public_key': settings.MERCADOPAGO_PUBLIC_KEY
    })

def payment_done(request):
    order_id = request.session.get('order_id')
    if order_id:
        order = get_object_or_404(Order, id=order_id)
        order.paid = True
        order.save()
    return render(request, 'orders/payment/done.html')

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def payment_canceled(request):
    return render(request, 'orders/payment/canceled.html')

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

@csrf_exempt
def payment_webhook(request):
    if request.method == 'POST':
        topic = request.GET.get('topic') or request.GET.get('type')
        payment_id = request.GET.get('id') or request.GET.get('data.id')
        
        # Mercado Pago sends data in different ways depending on version/config
        # We need to robustly find the ID
        
        if not payment_id and request.body:
             import json
             try:
                 data = json.loads(request.body)
                 payment_id = data.get('data', {}).get('id') or data.get('id')
             except:
                 pass

        print(f"WEBHOOK RECEIVED: Topic={topic}, ID={payment_id}")

        if payment_id:
            sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)
            try:
                payment_info = sdk.payment().get(payment_id)
                payment = payment_info.get("response", {})
                
                if payment:
                    external_reference = payment.get("external_reference")
                    status = payment.get("status")
                    
                    print(f"WEBHOOK INFO: Order={external_reference}, Status={status}")
                    
                    if external_reference:
                        try:
                            order = Order.objects.get(id=external_reference)
                            order.payment_status = status
                            
                            # Si el estado cambia a aprobado y no estaba pagado antes
                            if status == 'approved' and not order.paid:
                                order.paid = True
                                order.save()
                                
                                # Enviar Email
                                subject = f'Pedido #{order.id} confirmado - Tienda Virtual'
                                message = f'Hola {order.first_name},\n\nTu pedido #{order.id} ha sido confirmado.\n\nGracias por tu compra.'
                                html_message = render_to_string('orders/email/paid_order.html', {'order': order})
                                
                                try:
                                    send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email], html_message=html_message)
                                    print(f"EMAIL SENT to {order.email}")
                                except Exception as e_mail:
                                    print(f"EMAIL ERROR: {e_mail}")
                                    
                            else:
                                order.save()
                                
                            print(f"ORDER UPDATED: {order.id} status is now {status}")
                        except Order.DoesNotExist:
                            print("ORDER NOT FOUND")
                            
            except Exception as e:
                print(f"WEBHOOK ERROR: {e}")

    return HttpResponse(status=200)
