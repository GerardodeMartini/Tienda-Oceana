from django import forms
from django.db import models
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'description', 'price', 'stock', 'brand', 'is_combo', 'components', 'image', 'is_active', 'is_on_sale']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'id': 'id_price'}),
            'components': forms.SelectMultiple(attrs={'class': 'component-selector', 'style': 'height: 200px;'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user and not self.user.is_superuser:
            # Filter brand choices based on group
            if self.user.groups.filter(name='Oceana Managers').exists():
                self.fields['brand'].choices = [
                    ('oceana', 'Océana'),
                    ('both', 'Ambos (Ecosistema)'),
                ]
                self.fields['components'].queryset = Product.objects.filter(models.Q(brand='oceana') | models.Q(brand='both'))
            elif self.user.groups.filter(name='Heiwa Managers').exists():
                self.fields['brand'].choices = [
                    ('heiwa', 'Heiwa'),
                    ('both', 'Ambos (Ecosistema)'),
                ]
                self.fields['components'].queryset = Product.objects.filter(models.Q(brand='heiwa') | models.Q(brand='both'))

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
