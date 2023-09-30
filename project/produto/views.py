from django.shortcuts import render, redirect
from .domain.repositories import product_repository, unit_repository
from .domain.services.CartService import CartService

def index(request):
    if request.method == 'GET':
        units = unit_repository.get_showcase()
        return render(request, 'index.html', {"units": units})

def view(request, slug):
    if request.method == 'GET':
        product = product_repository.get_by_slug(slug)
        return render(request, 'view.html', {"product": product})

def add_to_cart(request):
    if request.method == 'GET':
        unit_id_param =  request.GET.get('id')
        quantity_param = request.GET.get('qty') or '1'

        unit = unit_repository.get_or_404(unit_id_param)

        cart = CartService(request)
        cart.add(unit, quantity_param)

        return redirect('produto:view', slug=unit.product.slug)        

def cart(request):
    context = {
        "unit": request.session.get("cart", {})
    }
    return render(request, "cart.html")