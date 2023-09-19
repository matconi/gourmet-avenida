from django.shortcuts import render
from .domain.repositories import product_repository, unit_repository

def index(request):
    if request.method == 'GET':
        units = unit_repository.get_showcase()
        return render(request, 'index.html', {"units": units})

def view(request, slug):
    if request.method == 'GET':
        product = product_repository.get_by_slug(slug)
        return render(request, 'view.html', {"product": product})
