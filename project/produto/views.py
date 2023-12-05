from django.shortcuts import render, redirect
from .domain.repositories import product_repository, unit_repository, category_repository
from .domain.services.CartService import CartService
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.http import JsonResponse

@login_required
def index(request):
    if request.method == 'GET':
        units = unit_repository.get_index()
        units_loaded = units[0:unit_repository.CARDS_PER_VIEW]

        json_data = {
            "urls": {
                "load_more": reverse('api_produto:load_more'),
                "add_to_cart": reverse('produto:add_to_cart'),
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

@login_required
def index_category(request, category_slug):
    if request.method == 'GET':
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

@login_required
def view(request, category_slug, unit_slug):
    if request.method == 'GET':
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

@login_required
@permission_required('produto.add_to_cart', raise_exception=True)
def add_to_cart(request):
    if request.method == 'GET':
        unit_id_param =  request.GET.get('id')
        quantity_param = request.GET.get('qty') or '1'

        unit = unit_repository.get_or_404(unit_id_param)

        cart = CartService(request)
        messages = cart.add(unit, quantity_param)

        return JsonResponse({
            "messages": messages
        })

@login_required
@permission_required('produto.add_one_to_cart', raise_exception=True)
def add_one_to_cart(request, pk: int):
    if request.method == 'GET':
        unit = unit_repository.get_or_404(pk)
        is_increment = request.GET.get('o') == '1'

        cart = CartService(request)
        cart.add(unit, 1 if is_increment else -1)

        return redirect('produto:cart')  

@login_required
@permission_required('produto.cart', raise_exception=True)
def cart(request):
    if request.method == 'GET':
        return render(request, "produto/cart.html")

@login_required
@permission_required('produto.clear_cart', raise_exception=True)
def clear_cart(request):
    if request.method == 'POST':
        cart = CartService(request)
        cart.clear()
        return redirect('produto:cart')

@login_required
@permission_required('produto.remove_from_cart', raise_exception=True)
def remove_from_cart(request):
    if request.method == 'POST':
        pk = request.POST.get('id')
        unit = unit_repository.get_or_404(pk)
        cart = CartService(request)
        cart.remove(unit)
        return redirect('produto:cart')