from allauth.account import signals
from django.dispatch import receiver
from .domain.services import messages_service

@receiver(signals.user_logged_in)
def user_logged_in_(request, user, **kwargs):
    if not user.phone:
        messages_service.uncomplete_register(request)