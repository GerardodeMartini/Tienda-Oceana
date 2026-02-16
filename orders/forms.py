from django import forms
from .models import Order
from cart.shipping import PROVINCES

class OrderCreateForm(forms.ModelForm):
    stat_province = forms.ChoiceField(choices=PROVINCES, label="Provincia")

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address',
                  'postal_code', 'city', 'stat_province']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'address': 'Dirección',
            'postal_code': 'Código Postal',
            'city': 'Ciudad',
        }
