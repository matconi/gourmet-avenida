from allauth.account.signals import user_logged_in, password_set, password_changed, password_reset
from django.dispatch import receiver
from usuario.domain.services import messages_service
from usuario.models import User
from usuario.domain.services import customer_service

@receiver([user_logged_in, password_set, password_changed, password_reset])
def reset_attempts(sender, request, user: User, **kwargs):
    if user.attempts > 0:
        user.attempts = 0
        user.save()