from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .forms import ProfileForm
from .domain.services import messages_service
from pedido.domain.repositories import order_unit_repository
from produto.domain.repositories import unit_repository
from gourmetavenida.utils import paginate
from .domain.services import payment_service
from .domain.repositories import payment_repository, user_repository, customer_repository
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST, require_http_methods

@require_http_methods(['GET', 'POST'])
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

@require_GET
def home(request):
    week_trends = order_unit_repository.get_week_trends()
    releases = unit_repository.get_releases()
    
    json_data = {
        "urls": {
            "add_from_list_to_cart": reverse('produto:add_from_list_to_cart')
        }
    }

    context = {
        "week_trends": week_trends,
        "releases": releases,
        "json_data": json_data
    }

    if request.user.has_perm('pedido.add_order'):
        again = order_unit_repository.get_again(request.user.user_customer)
        context["again"] = again

    return render(request, 'usuario/home.html', context)

@require_GET
@login_required
@permission_required('usuario.payments', raise_exception=True)
def payments(request):
    kwargs = payment_service.filter_payments(request)

    payments = payment_repository.get_customer_payments(request.user.user_customer, kwargs)

    context = {
        "page_obj": paginate(request, payments)
    }
    return render(request, 'usuario/payments.html', context)

@require_GET
@login_required
@permission_required('usuario.favorites', raise_exception=True)
def favorites(request):
    units = unit_repository.get_customer_favorites(request.user.user_customer)
    units_loaded = units[0:unit_repository.CARDS_PER_VIEW]

    json_data = {
        "urls": {
            "load_more": reverse('api_usuario:load_more_favorites'),
            "add_from_list_to_cart": reverse('produto:add_from_list_to_cart')
        },
        "permissions": {
            "add_from_list_to_cart": request.user.has_perm('produto.add_from_list_to_cart')
        }
    }

    context = {
        "units_loaded": units_loaded, 
        "json_data": json_data
    }
    return render(request, 'usuario/favorites.html', context)

@require_POST
@login_required
@permission_required('usuario.add_favorite', raise_exception=True)
def add_favorive(request):
    unit_id = request.POST.get('id')

    unit = unit_repository.get_or_404(unit_id)
    customer_repository.add_favorite(request.user.user_customer, unit)

    messages = {
        "success": [messages_service.favorite_added(unit)],
    }
    return JsonResponse(
        {"messages": messages}
    )

@require_POST
@login_required
@permission_required('usuario.remove_favorite', raise_exception=True)
def remove_favorive(request):
    unit_id = request.POST.get('id')

    unit = unit_repository.get_or_404(unit_id)
    customer_repository.remove_favorite(request.user.user_customer, unit)

    messages = {
        "success": [messages_service.favorite_removed(unit)],
    }
    return JsonResponse(
        {"messages": messages}
    )