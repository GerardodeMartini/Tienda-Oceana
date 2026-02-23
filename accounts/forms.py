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
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class CustomAuthForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            
            # Django's authenticate() returns None for inactive users in recent versions.
            # So, if authenticate fails, let's manually check if the user exists but is inactive.
            if self.user_cache is None:
                from django.db.models import Q
                user = User.objects.filter(Q(username=username) | Q(email=username)).first()
                if user and not user.is_active:
                    raise ValidationError(
                        "Esta cuenta está inactiva. Por favor verifique su correo para validarla.",
                        code='inactive',
                    )
            
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
