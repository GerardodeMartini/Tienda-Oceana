from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.conf import settings
from django.contrib import messages
import urllib.request
import urllib.parse
import json
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST) # Prioritize form validation to keep data if captcha fails
        
        # Turnstile Validation
        turnstile_response = request.POST.get('cf-turnstile-response')
        
        if turnstile_response:
            secret = settings.TURNSTILE_SECRET_KEY
            url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
            data = urllib.parse.urlencode({'secret': secret, 'response': turnstile_response}).encode()
            
            try:
                req = urllib.request.Request(url, data=data)
                response = urllib.request.urlopen(req)
                result = json.loads(response.read().decode())
                
                if not result.get('success'):
                   messages.error(request, 'Error de verificación de seguridad (Captcha). Intenta de nuevo.')
                   # We don't save yet
                elif user_form.is_valid():
                    new_user = user_form.save()
                    login(request, new_user)
                    return redirect('store:product_list')
            except Exception as e:
                 messages.error(request, 'Error al conectar con el servicio de seguridad.')
        else:
             messages.error(request, 'Por favor completa la verificación de seguridad.')

    else:
        user_form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'turnstile_site_key': settings.TURNSTILE_SITE_KEY
    })
