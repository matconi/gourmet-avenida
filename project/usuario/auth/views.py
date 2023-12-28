from django.shortcuts import redirect
from django.urls import reverse
from usuario.domain.services import messages_service
from allauth.account.views import PasswordResetDoneView, PasswordResetFromKeyDoneView, LogoutView, _ajax_response
from produto.domain.services import CartService
import copy

class CustomPasswordResetDoneView(PasswordResetDoneView):
    def get(self, *args, **kwargs):
        messages_service.password_reset_done(self.request)
        return redirect('account_login')

password_reset_done = CustomPasswordResetDoneView.as_view()

class CustomLogoutView(LogoutView):
    def post(self, *args, **kwargs):
        cart = self.request.session.get('cart')
        cart_copy = copy.deepcopy(cart)
        logout = super(CustomLogoutView, self).post(*args, **kwargs)
        self.request.session["cart"] = cart_copy
        self.request.session.modified = True
        return logout

logout = CustomLogoutView.as_view()