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
            
            if request.user.is_authenticated:
                order.user = request.user
            
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
        # Pre-fill form if user is authenticated
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
            # Try to get phone from profile
            if hasattr(request.user, 'profile') and request.user.profile.phone_number:
                initial_data['phone'] = request.user.profile.phone_number
                
        form = OrderCreateForm(initial=initial_data)
        
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
                                
                                # Enviar Email al Comprador
                                subject = f'Pedido #{order.id} confirmado - Tienda Virtual'
                                message = f'Hola {order.first_name},\n\nTu pedido #{order.id} ha sido confirmado.\n\nGracias por tu compra.'
                                html_message = render_to_string('orders/email/paid_order.html', {'order': order})
                                
                                try:
                                    send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email], html_message=html_message)
                                    print(f"BUYER EMAIL SENT to {order.email}")
                                except Exception as e_mail:
                                    print(f"BUYER EMAIL ERROR: {e_mail}")

                                # Enviar Email al Vendedor (Admin)
                                admin_subject = f'Nuevo Pedido #{order.id} - {order.first_name} {order.last_name}'
                                admin_message = f'Nuevo pedido confirmado.\nID: {order.id}\nTotal: ${order.get_total_cost()}'
                                html_admin_message = render_to_string('orders/email/admin_new_order.html', {'order': order})
                                
                                # Asumiendo que el mail del vendedor es el mismo que EMAIL_HOST_USER o uno fijo
                                seller_email = settings.EMAIL_HOST_USER 
                                
                                try:
                                    send_mail(admin_subject, admin_message, settings.EMAIL_HOST_USER, [seller_email], html_message=html_admin_message)
                                    print(f"SELLER EMAIL SENT to {seller_email}")
                                except Exception as e_admin_mail:
                                    print(f"SELLER EMAIL ERROR: {e_admin_mail}")
                                    
                            else:
                                order.save()
                                
                            print(f"ORDER UPDATED: {order.id} status is now {status}")
                        except Order.DoesNotExist:
                            print("ORDER NOT FOUND")
                            
            except Exception as e:
                print(f"WEBHOOK ERROR: {e}")

    return HttpResponse(status=200)

from django.contrib.auth.decorators import login_required

@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order/user_list.html', {'orders': orders})

from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_staff)
def admin_order_list(request):
    orders = Order.objects.all().order_by('-created')
    return render(request, 'orders/order/admin_list.html', {'orders': orders})

@user_passes_test(lambda u: u.is_staff)
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order/admin_detail.html', {'order': order})

from django.contrib import messages

@user_passes_test(lambda u: u.is_staff)
def admin_order_toggle_shipped(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.shipped = not order.shipped
        order.save()
        status = "ENVIADO" if order.shipped else "NO ENVIADO"
        messages.success(request, f'Estado de envío actualizado a: {status}')
    return redirect('orders:admin_order_detail', order_id=order.id)
