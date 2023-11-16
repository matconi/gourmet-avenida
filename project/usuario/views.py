from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .domain.services import messages_service
from pedido.domain.repositories import order_unit_repository
from produto.domain.repositories import unit_repository
from gourmetavenida.utils import paginate
from .domain.services import payment_service
from .domain.repositories import payment_repository
from produto.domain.repositories import unit_repository

@login_required
def profile(request):
    user = request.user

    if request.method == 'GET':
        form = ProfileForm(
            initial={
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
            }
        )

        context = {
            "form": form,
            "user": user
        }
        return render(request, "usuario/profile.html", context)
        
    elif request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages_service.updated_profile(request)
        
        return redirect('usuario:profile')

def home(request):
    if request.method == 'GET':
        week_trends = order_unit_repository.get_week_trends()
        releases = unit_repository.get_releases()

        context = {
            "week_trends": week_trends,
            "releases": releases
        }

        if request.user.is_authenticated:
            again = order_unit_repository.get_again(request.user.user_customer)
            context["again"] = again

        return render(request, 'usuario/home.html', context)

@login_required
def payments(request):
    if request.method == 'GET':
        kwargs = payment_service.filter_payments(request)

        payments = payment_repository.get_customer_payments(request.user.user_customer, kwargs)

        context = {
           "page_obj": paginate(request, payments)
        }
        return render(request, 'usuario/payments.html', context)

@login_required
def favorites(request):
    if request.method == 'GET':
        units = unit_repository.get_customer_favorites(request.user.user_customer)
        return render(request, 'usuario/favorites.html', {"units": units})