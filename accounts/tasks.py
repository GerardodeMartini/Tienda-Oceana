from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
User = get_user_model()

@shared_task
def cleanup_inactive_users():
    """
    Elimina los usuarios que no han activado su cuenta por correo
    después de más de 1 año (365 días) de haberse registrado.
    Se ejecuta automáticamente según la programación de Celery Beat.
    """
    cutoff_date = timezone.now() - timedelta(days=365)
    
    # Filtramos usuarios Inactivos, no-Staff, creados antes de la fecha límite
    users_to_delete = User.objects.filter(
        is_active=False,
        is_staff=False,
        is_superuser=False,
        date_joined__lt=cutoff_date
    )
    
    count = users_to_delete.count()
    if count > 0:
        logger.info(f"Borrando {count} cuentas de usuario inactivas...")
        users_to_delete.delete()
        logger.info(f"Limpieza finalizada.")
    else:
        logger.info("No se encontraron cuentas inactivas para limpiar.")
        
    return count
