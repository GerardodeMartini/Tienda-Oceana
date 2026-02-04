from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price', 'stock', 'created', 'updated', 'is_active']
    list_filter = ['is_active', 'created', 'updated']
    list_editable = ['price', 'stock', 'is_active']
    prepopulated_fields = {'slug': ('title',)}
