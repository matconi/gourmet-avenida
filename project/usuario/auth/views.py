from django.shortcuts import redirect
from django.urls import reverse
from usuario.domain.services import messages_service
from allauth.account.views import PasswordResetDoneView, PasswordResetFromKeyDoneView, LogoutView, _ajax_response
from copy import deepcopy

class CustomPasswordResetDoneView(PasswordResetDoneView):
    def get(self, *args, **kwargs):
        messages_service.password_reset_done(self.request)
        return redirect('account_login')

password_reset_done = CustomPasswordResetDoneView.as_view()

class CustomPasswordResetFromKeyDoneView(PasswordResetFromKeyDoneView):
    def get(self, *args, **kwargs):
        return redirect('account_login')

password_reset_from_key_done = CustomPasswordResetFromKeyDoneView.as_view()

class CustomLogoutView(LogoutView):
    def post(self, *args, **kwargs):
        url = self.get_redirect_url()
        if self.request.user.is_authenticated:
            cart = copy.deepcopy(Cart(request).cart)
            self.logout()
            session = self.request.session
            session["cart"] = cart
            session.modified = True
            response = redirect(url)
        return _ajax_response(self.request, response)