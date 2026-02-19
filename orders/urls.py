from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('payment/process/', views.payment_process, name='payment_process'),
    path('payment/done/', views.payment_done, name='payment_done'),
    path('payment/canceled/', views.payment_canceled, name='payment_canceled'),
    path('webhook/', views.payment_webhook, name='payment_webhook'),
    path('my-orders/', views.user_orders, name='user_orders'),
    path('admin/orders/', views.admin_order_list, name='admin_order_list'),
    path('admin/orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/orders/<int:order_id>/toggle-shipped/', views.admin_order_toggle_shipped, name='admin_order_toggle_shipped'),
]
