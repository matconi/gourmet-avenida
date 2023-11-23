from .domain.repositories import category_repository

def categories(request):
    return {"categories": category_repository.get_all()}