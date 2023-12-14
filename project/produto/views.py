from django.shortcuts import render, redirect
from .domain.repositories import product_repository, unit_repository, category_repository
from .domain.services import CartService
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.core.validators import ValidationError
from gourmetavenida.utils import try_method
from .templatetags import produto_pipe

@require_GET
@login_required
def index(request):
    units = unit_repository.get_index()
    units_loaded = units[0:unit_repository.CARDS_PER_VIEW]

    json_data = {
        "urls": {
            "load_more": reverse('api_produto:load_more'),
            "add_to_cart": reverse('produto:add_to_cart')
        },
        "permissions": {
            "add_to_cart": request.user.has_perm('produto.add_to_cart')
        }
    }

    context = {
        "units_loaded": units_loaded, 
        "json_data": json_data
    }

    return render(request, 'produto/index.html', context)

@require_GET
@login_required
def index_category(request, category_slug):
    category_selected = category_repository.get_by_slug(category_slug)

    units = unit_repository.get_index_category(category_slug)
    units_loaded = units[0:unit_repository.CARDS_PER_VIEW]

    json_data = {
        "urls": {
            "load_more": reverse('api_produto:load_more_category', args=[category_selected.slug]),
            "add_to_cart": reverse('produto:add_to_cart'),
        },
        "permissions": {
            "add_to_cart": request.user.has_perm('produto.add_to_cart')
        }
    }

    context = {
        "units_loaded": units_loaded,
        "category_selected": category_selected,
        "json_data": json_data
    }

    return render(request, 'produto/index_category.html', context)

@require_GET
@login_required
def view(request, category_slug, unit_slug):
    product = product_repository.get_by_slug(unit_slug)
    units_category = unit_repository.get_related_category(category_slug, product.id)[0:10]
    json_data = {
        "urls": {
            "view_product": reverse('api_produto:view_product', args=[product.slug]),
            "add_favorite": reverse('usuario:add_favorite'),
            "remove_favorite": reverse('usuario:remove_favorite'),
            "add_to_cart": reverse('produto:add_to_cart'),
        },
        "permissions": {
            "add_favorite": request.user.has_perm('usuario.add_favorite'),
            "remove_favorite": request.user.has_perm('usuario.remove_favorite'),
            "add_to_cart": request.user.has_perm('produto.add_to_cart'),
        }   
    }

    context = {
        "product": product,
        "units_category": units_category,
        "json_data": json_data    
    }

    return render(request, 'produto/view.html', context)

@require_GET
@login_required
@permission_required('produto.cart', raise_exception=True)
def cart(request):
    json_data = {
        "urls": {
            "increment_cart": reverse('produto:increment_cart'),
            "decrement_cart": reverse('produto:decrement_cart'),
            "clean_cart": reverse('produto:clean_cart'),
            "remove_from_cart": reverse('produto:remove_from_cart'),
        }
    }

    context = {
        "json_data": json_data
    }
    return render(request, "produto/cart.html", context)

@require_GET
@login_required
@permission_required('produto.add_to_cart', raise_exception=True)
def add_to_cart(request):
    unit_id_param = request.GET.get('id')
    quantity_param = request.GET.get('qty', '1')
    unit = unit_repository.get_or_404(unit_id_param)

    cart = CartService(request)
    try_method(cart, cart.add, [unit, quantity_param])
    messages = cart.get_messages()

    return JsonResponse({
        "messages": messages,
        "refresh_cart": {
            "total_in_cart": produto_pipe.total_in_cart(cart.cart),
        }
    })

@require_GET
@login_required
@permission_required('produto.increment_cart', raise_exception=True)
def increment_cart(request):
    unit_id_param = request.GET.get('id')

    unit = unit_repository.get_or_404(unit_id_param)

    cart = CartService(request)
    try_method(cart, cart.increment, [unit])
    messages = cart.get_messages()

    return JsonResponse({
        "messages": messages,
        "refresh_cart": {
            "total_in_cart": produto_pipe.total_in_cart(cart.cart),
            "total_price_in_cart": produto_pipe.total_price_in_cart(cart.cart),
            "unit_in_cart": cart.cart.get(unit_id_param)
        }
    })

@require_GET
@login_required
@permission_required('produto.decrement_cart', raise_exception=True)
def decrement_cart(request):
    unit_id_param = request.GET.get('id')
    unit = unit_repository.get_or_404(unit_id_param)

    cart = CartService(request)
    try_method(cart, cart.decrement, [unit])
    messages = cart.get_messages()

    return JsonResponse({
        "messages": messages,
        "refresh_cart": {
            "total_in_cart": produto_pipe.total_in_cart(cart.cart),
            "total_price_in_cart": produto_pipe.total_price_in_cart(cart.cart),
            "unit_in_cart": cart.cart.get(unit_id_param)
        }
    })

@require_POST
@login_required
@permission_required('produto.clean_cart', raise_exception=True)
def clean_cart(request):
    cart = CartService(request)
    cart.clean()
    messages = cart.get_messages()

    return JsonResponse({
        "messages": messages,
        "refresh_cart": {
            "total_in_cart": 0,
        }
    })

@require_POST
@login_required
@permission_required('produto.remove_from_cart', raise_exception=True)
def remove_from_cart(request):
    unit_id_param = request.POST.get('id')
    cart = CartService(request)
    try_method(cart, cart.remove, [unit_id_param])
    messages = cart.get_messages()

    return JsonResponse({
        "messages": messages,
        "refresh_cart": {
            "total_in_cart": produto_pipe.total_in_cart(cart.cart),
            "total_price_in_cart": produto_pipe.total_price_in_cart(cart.cart),
        }
    })
