from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirmar Contraseña', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        
    def clean_password_confirm(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_confirm']:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return cd['password_confirm']
