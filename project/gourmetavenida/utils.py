from django.core.paginator import Paginator, Page
from datetime import datetime
from typing import Callable
from django.core.validators import ValidationError
from django.contrib import messages

def paginate(request, queryset, intens_per_page=10) -> Page:
    paginator = Paginator(queryset, intens_per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)

def is_ajax(request) -> bool:
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

def str_date_to_datetime(date: str, date_format: str="%d/%m/%Y", datetime_format: str="%Y-%m-%d %H:%M"):
    try:
        return datetime.strptime(date, date_format).strftime(datetime_format)
    except Exception as e:
        print(e)

def refresh_if_invalid(instance, method: Callable, args: list=[]) -> None:
    """ Instance must have 'messages' dict attribute with 'danger' key, 
    wich contains an error list to be displayed for user
    """
    try:
        method(*args)
    except ValidationError as e:
        instance.messages["danger"].append(e.message)

def reload_if_invalid(request, instance, method: Callable, args: list=[]) -> None:
    try:
        method(*args)
    except ValidationError as e:
        messages.error(request, e.message)