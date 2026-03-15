from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
import urllib.request
import urllib.parse
import json
from .forms import UserRegistrationForm

User = get_user_model()

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
                    new_user = user_form.save(commit=False)
                    new_user.is_active = False # Require email verification
                    new_user.save()
                    
                    # Generar token y link de activacion
                    current_site = get_current_site(request)
                    mail_subject = 'Activa tu cuenta en Tienda Océana & Heiwa'
                    uid = urlsafe_base64_encode(force_bytes(new_user.pk))
                    token = default_token_generator.make_token(new_user)
                    activation_link = f"http://{current_site.domain}/accounts/activate/{uid}/{token}/"
                    
                    message = render_to_string('accounts/email/activation_email.html', {
                        'user': new_user,
                        'activation_link': activation_link,
                    })
                    
                    try:
                        send_mail(mail_subject, '', settings.DEFAULT_FROM_EMAIL, [new_user.email], html_message=message)
                        print(f"ACTIVATION EMAIL SENT to {new_user.email}")
                    except Exception as e:
                        print(f"Error enviando email de activación a {new_user.email}: {e}")
                    
                    return render(request, 'accounts/registration_pending.html', {'email': new_user.email, 'username': new_user.username})
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

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, '¡Tu cuenta ha sido verificada exitosamente! Ya puedes realizar compras.')
        return redirect('store:product_list')
    else:
        messages.error(request, 'El enlace de activación es inválido o ha expirado. Por favor, regístrate nuevamente.')
        return redirect('accounts:register')
