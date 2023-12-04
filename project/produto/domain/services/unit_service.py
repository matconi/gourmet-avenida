

def filter_units(request) -> dict:
    name = request.GET.get('q', '')
    category_id = request.GET.get('cat', '')

    kwargs = {}
    _filter_name(name, kwargs)
    _filter_category(category_id, kwargs)
    
    return kwargs

def _filter_name(name: str, kwargs: dict) -> None:
    if name.strip():
        kwargs["name__icontains"] = name

def _filter_category(category_id: str, kwargs: dict) -> None:
    if category_id.strip():
        kwargs["product__category__id"] = category_id
