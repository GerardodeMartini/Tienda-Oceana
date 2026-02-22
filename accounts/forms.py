from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    phone_number = forms.CharField(max_length=20, required=True, label='Teléfono', 
                                  widget=forms.TextInput(attrs={'placeholder': 'Ej: +54 9 11 ...'}))
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
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.create(user=user, phone_number=self.cleaned_data['phone_number'])
        return user

from django.contrib.auth.forms import AuthenticationForm

class CustomAuthForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                "Esta cuenta está inactiva.",
                code='inactive',
            )
        super().confirm_login_allowed(user)
