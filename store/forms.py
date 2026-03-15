from django import forms
from django.db import models
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'description', 'price', 'original_price', 'stock', 'brand', 'is_combo', 'components', 'image', 'is_active', 'is_on_sale']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'id': 'id_price'}),
            'original_price': forms.HiddenInput(attrs={'id': 'id_original_price'}),
            'components': forms.SelectMultiple(attrs={'class': 'component-selector', 'style': 'height: 200px;'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user and not self.user.is_superuser:
            # Filter brand choices based on group
            if self.user.groups.filter(name='Oceana Managers').exists():
                self.fields['brand'].choices = [
                    (Product.BRAND_OCEANA, 'Océana'),
                    (Product.BRAND_BOTH, 'Ambos (Ecosistema)'),
                ]
                self.fields['components'].queryset = Product.objects.filter(
                    models.Q(brand=Product.BRAND_OCEANA) | models.Q(brand=Product.BRAND_BOTH)
                )
            elif self.user.groups.filter(name='Heiwa Managers').exists():
                self.fields['brand'].choices = [
                    (Product.BRAND_HEIWA, 'Heiwa'),
                    (Product.BRAND_BOTH, 'Ambos (Ecosistema)'),
                ]
                self.fields['components'].queryset = Product.objects.filter(
                    models.Q(brand=Product.BRAND_HEIWA) | models.Q(brand=Product.BRAND_BOTH)
                )

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
