from django.shortcuts import render
from .domain.repositories import product_repository

def index(request):
    if request.method == 'GET':
        units = product_repository.get_all()
        return render(request, 'index.html', {"units": units})