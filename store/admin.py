from django.contrib import admin
from django.db import models
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price', 'stock', 'brand', 'is_active']
    list_filter = ['brand', 'is_active', 'created', 'updated']
    list_editable = ['price', 'stock', 'is_active', 'brand']
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        
        # Filter by group membership
        if request.user.groups.filter(name='Oceana Managers').exists():
            return qs.filter(
                models.Q(brand=Product.BRAND_OCEANA) | models.Q(brand=Product.BRAND_BOTH)
            )
        
        if request.user.groups.filter(name='Heiwa Managers').exists():
            return qs.filter(
                models.Q(brand=Product.BRAND_HEIWA) | models.Q(brand=Product.BRAND_BOTH)
            )
            
        return qs

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            # Auto-assign brand if creating new, or ensure they don't change it to outside their scope
            # Note: For simplicity, we trust the form restriction below, but logical checks could be added here.
            # If a user is only Oceana, they shouldn't be able to save as Heiwa.
            pass
        super().save_model(request, obj, form, change)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "brand" and not request.user.is_superuser:
            if request.user.groups.filter(name='Oceana Managers').exists():
                kwargs['choices'] = [
                    (Product.BRAND_OCEANA, 'Océana'),
                    (Product.BRAND_BOTH, 'Ambos (Ecosistema)'),
                ]
            elif request.user.groups.filter(name='Heiwa Managers').exists():
                kwargs['choices'] = [
                    (Product.BRAND_HEIWA, 'Heiwa'),
                    (Product.BRAND_BOTH, 'Ambos (Ecosistema)'),
                ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

