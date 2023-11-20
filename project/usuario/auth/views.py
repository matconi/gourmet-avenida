from django.shortcuts import redirect
from django.urls import reverse
from usuario.domain.services import messages_service
from allauth.account.views import PasswordResetDoneView, PasswordResetFromKeyDoneView

class CustomPasswordResetDoneView(PasswordResetDoneView):
    def get(self, *args, **kwargs):
        messages_service.password_reset_done(self.request)
        return redirect('account_login')

password_reset_done = CustomPasswordResetDoneView.as_view()

class CustomPasswordResetFromKeyDoneView(PasswordResetFromKeyDoneView):
    def get(self, *args, **kwargs):
        return redirect('account_login')

password_reset_from_key_done = CustomPasswordResetFromKeyDoneView.as_view()