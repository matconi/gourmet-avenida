from django import forms
from .models import Order, OrderUnit
from usuario.models import Payment, Customer
from usuario.domain.repositories import payment_repository, customer_repository
from .domain.services import messages_service
from .domain.services import OrderService
from usuario.domain.services import customer_service
from pedido.domain.repositories import order_unit_repository
from datetime import date
from typing import List
from django.core.validators import ValidationError

class OrderAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OrderAdminForm, self).__init__(*args, **kwargs)
        self.fields["total_price"].help_text ='Cálculo Automático'
        self.fields["total_quantity"].help_text ='Cálculo Automático'
        self.__is_paid()
            
    is_paid = forms.BooleanField(label='Pago', required=False,
        help_text='Cria um pagamento por PIX junto à compra finalizada.'
    )

    def __is_paid(self) -> None:
        if self.instance.payment:
            self.fields["is_paid"].widget.attrs.update({"checked": True})

    def clean(self):
        self.cleaned_data = super(OrderAdminForm, self).clean() 
        self.__validate_finished()
        OrderService.validate_limit(self.cleaned_data["customer"])
        self.__validate_booking_date()
        if not self.instance.id:
            self.__validate_initial_status()
        else:
            self.__validate_book_only_create()
            
    def __validate_finished(self) -> None:
        if self.initial.get("status") == Order.Status.FINISHED and self.cleaned_data["status"] == Order.Status.FINISHED:
            raise ValidationError("Não é possível editar um pedido finalizado")
        
    def __validate_booking_date(self) -> None:
        if self.cleaned_data["status"] == Order.Status.BOOKED:
            if not self.cleaned_data["booked_upto"]:
                raise ValidationError("Para reservar um pedido, é necessário informar a data de expiração!")
                
            today = date.today()
            exp = self.instance.booked_upto.date()
            if exp < today:
                raise ValidationError("O pedido não pode ser reservado com a data anterior a hoje!")

            if self.initial.get('booked_upto') and not self.cleaned_data["booked_upto"]:
                raise ValidationError("A data de expiração não pode ser apagada.")

    def __validate_initial_status(self) -> None:
        status_denied = [Order.Status.REPROVED, Order.Status.EXPIRED, Order.Status.ABANDONED]
        if self.cleaned_data["status"] in status_denied:
            raise ValidationError("Não é possível criar um pedido expirado, reprovado ou cancelado.")

    def save(self, *args, **kwargs):
        if not self.instance.id:
            self.instance = super(OrderAdminForm, self).save(*args, **kwargs) 
            self.__change_unit_booking()
        else:
            self.instance = super(OrderAdminForm, self).save(*args, **kwargs)  
            self.__booking_changed()          
        return self.instance

    def __validate_book_only_create(self) -> None:
        if self.instance.id and 'status' in self.changed_data and self.cleaned_data["status"] == Order.Status.BOOKED:
            raise ValidationError("Uma reserva só pode ser feita ao criar um pedido, não ao editar.")

    def set_totals(self, order_units: List[OrderUnit]) -> None:
        self.instance.set_total_price(order_units)
        self.instance.set_total_quantity(order_units)
    
    def __change_unit_booking(self) -> None:
        if self.cleaned_data["status"] == Order.Status.BOOKED:
            order_units = order_unit_repository.get_by_order(self.instance)
            OrderService.up_boked(order_units)
            messages_service.increased_booking(self.request)

    def __booking_changed(self) -> None:
        if self.initial.get("status") == Order.Status.BOOKED and self.cleaned_data["status"] != Order.Status.BOOKED:
            order_units = order_unit_repository.get_by_order(self.instance)
            OrderService.down_booked(order_units)
            messages_service.removed_booking(self.request)

    def bind_payment(self) -> None:
        if (
            self.cleaned_data["status"] == Order.Status.FINISHED 
            and (self.__not_premium_or_paid())
            and not self.instance.payment
        ):
            payment = payment_repository.bind_order_payment(self.instance)
            self.instance.payment = payment
            self.instance.save()
            messages_service.binded_order_payment(self.request, payment)
            self.__pay_bill(payment)
    
    def __not_premium_or_paid(self) -> bool:
        return not self.instance.customer.is_premium() or self.cleaned_data["is_paid"]

    def __pay_bill(self, payment: Payment) -> None:
        if self.instance.customer.is_premium():
            customer: Customer = customer_repository.pay_bill(payment)

    def buy_bill(self) -> None:
        if (
            self.cleaned_data["status"] == Order.Status.FINISHED 
            and self.instance.customer.is_premium()
            and not self.instance.payment
        ):
            customer = customer_repository.buy_bill(self.instance.customer, self.instance.total_price)
            messages_service.buyed_bill(self.request, customer, self.instance.total_price)

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js',
            '//cdnjs.cloudflare.com/ajax/libs/jquery.mask/1.14.16/jquery.mask.min.js',
            'js/admin-shared.js',
        )

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ('payment',)

class OrderUnitAdminForm(forms.ModelForm):
    def clean(self):
        raise ValidationError("É possível adicionar ou editar os itens do pedido apenas pelo formulário de pedido.")

    class Meta:
        model = OrderUnit
        fields = '__all__'