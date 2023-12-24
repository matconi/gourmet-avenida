from django import forms
from .models import Order
from django.core.validators import ValidationError
from usuario.models import Payment
from django.contrib import messages
from django.utils.html import format_html
from django.conf import settings
from usuario.domain.repositories import payment_repository
from .domain.services import messages_service
from .domain.services import OrderService
from pedido.domain.repositories import order_unit_repository
from gourmetavenida.utils import str_date_to_datetime
from datetime import date

class OrderAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OrderAdminForm, self).__init__(*args, **kwargs)
        self.fields["total_price"].help_text ='Cálculo Automático'
        self.fields["total_quantity"].help_text ='Cálculo Automático'

    is_paid = forms.BooleanField(label='Pago ', required=False,
        help_text='Cria um pagamento por PIX junto à compra.'
    )

    def save(self, *args, **kwargs):
        self.__validate_booking_date()
        if not self.instance.id:
            self.__validate_initial_status()
            self.instance = super(OrderAdminForm, self).save(*args, **kwargs)     
            self.__change_unit_booking()
        else:
            self.__validate_book_only_create()
            self.instance = super(OrderAdminForm, self).save(*args, **kwargs)    
            self.__booking_changed()
        self.__bind_payment()
        return self.instance

    def __validate_booking_date(self) -> None:
        if self.cleaned_data["status"] == Order.Status.BOOKED:
            if not self.cleaned_data["booked_upto"]:
                raise forms.ValidationError("Para reservar um pedido, é necessário informar a data de expiração!")
                
            today = date.today()
            exp = self.instance.booked_upto.date()
            if exp < today:
                raise forms.ValidationError("O pedido não pode ser reservado com a data anterior a hoje!")

    def __validate_initial_status(self) -> None:
        status_denied = [Order.Status.REPROVED, Order.Status.EXPIRED, Order.Status.ABANDONED]
        if self.cleaned_data["status"] in status_denied:
            raise forms.ValidationError("Não é possível criar um pedido expirado, reprovado ou cancelado.")

    def __change_unit_booking(self) -> None:
        if self.cleaned_data["status"] == Order.Status.BOOKED:
            order_units = order_unit_repository.get_by_order(self.instance)
            OrderService.up_boked(order_units)
            messages_service.increased_booking(self.request)

    def __validate_book_only_create(self) -> None:
        if self.instance.id and 'status' in self.changed_data and self.cleaned_data["status"] == Order.Status.BOOKED:
            raise forms.ValidationError("Uma reserva só pode ser feita ao criar um pedido, não ao editar.")

    def __booking_changed(self) -> None:
        if self.initial.get("status") == Order.Status.BOOKED and self.cleaned_data["status"] != Order.Status.BOOKED:
            order_units = order_unit_repository.get_by_order(self.instance)
            OrderService.down_booked(order_units)
            messages_service.removed_booking(self.request)

    def __bind_payment(self) -> None:
        if (
            self.cleaned_data["status"] == Order.Status.FINISHED 
            and (self.__not_premium_or_paid())
            and not self.instance.payment
        ):
            payment = payment_repository.bind_order_payment(self.cleaned_data, self.instance)
            self.instance.payment = payment
            messages_service.binded_order_payment(self.request, payment)

    def __not_premium_or_paid(self) -> bool:
        return self.instance.customer.user is None or not self.instance.customer.user.has_perm('pedido.add_order') or self.cleaned_data["is_paid"]

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ('payment',)