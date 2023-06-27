from django.core.mail import send_mass_mail

from config import celery_app

from .models import Notification, User


@celery_app.task()
def get_users_count():
    """Batches notifications to be sent to admins."""
    pending = Notification.objects.get_queryset(has_sent=False)
    recipient_emails = [u.email for u in User.objects.all()]
    pending = [
        (
            "Hola! Alguien ha modificado un producto",
            f"{notif.user.email} ha modificado {notif.product.name}",
            "mariomanza150@gmail.com",
            recipient_emails,
        )
        for notif in pending
    ]

    return send_mass_mail(pending, fail_silently=False)
