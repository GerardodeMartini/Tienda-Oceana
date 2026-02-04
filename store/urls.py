from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('dashboard/create/', views.product_create, name='product_create'),
    path('dashboard/edit/<int:product_id>/', views.product_edit, name='product_edit'),
    path('dashboard/category/create/', views.category_create, name='category_create'),
]
