from typing import List
from . import messages_service
from produto.models.Unit import Unit
from gourmetavenida.utils import str_date_to_datetime

def filter_units(request) -> dict:
    name = request.GET.get('q', '')

    kwargs = {}
    _filter_name(name, kwargs)
    
    return kwargs

def _filter_name(name: str, kwargs: dict) -> None:
    if name.strip():
        kwargs["name__icontains"] = name
