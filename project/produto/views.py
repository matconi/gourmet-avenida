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

def add_one_to_cart(request, pk: int):
    if request.method == 'GET':
        unit = unit_repository.get_or_404(pk)
        is_increment = request.GET.get('o') == '1'

        cart = CartService(request)
        cart.add(unit, 1 if is_increment else -1)

        return redirect('produto:cart')  

def cart(request):
    if request.method == 'GET':
        return render(request, "cart.html")

def clear_cart(request):
    if request.method == 'POST':
        cart = CartService(request)
        cart.clear()
        return redirect('produto:cart')

def remove_from_cart(request):
    if request.method == 'POST':
        pk = request.POST.get('id')
        unit = unit_repository.get_or_404(pk)
        cart = CartService(request)
        cart.remove(pk, unit)
        return redirect('produto:cart')