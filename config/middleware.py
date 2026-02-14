from django.utils.deprecation import MiddlewareMixin

class BrandMiddleware(MiddlewareMixin):
    """
    Middleware para detectar la marca (Oceana o Heiwa) basada en la URL
    y establecer el tema en la sesión.
    """
    def process_request(self, request):
        path = request.path
        
        # Detectar tema basado en el prefijo de la URL
        if path.startswith('/oceana/'):
            request.session['theme'] = 'oceana'
        elif path.startswith('/heiwa/'):
            request.session['theme'] = 'heiwa'
        else:
            # Si estamos en la raíz o cualquier otra URL no específica de marca
            # Mantenemos el tema actual si existe, o volvemos al default 'ecosystem'
            # (Opcional: forzar 'ecosystem' si salimos de las zonas de marca)
            if 'theme' not in request.session:
                request.session['theme'] = 'ecosystem'
            
            # Si queremos que volver al root restablezca al ecosistema:
            if path == '/':
                 request.session['theme'] = 'ecosystem'

        return None
