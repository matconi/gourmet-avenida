from . import messages_service
from produto.models.Unit import Unit
from gourmetavenida.utils import str_date_to_datetime

def filter_payments(request) -> dict:
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    method = request.GET.get('method')

    kwargs = {}
    _filter_date_time(start_date, end_date, kwargs)
    _filter_method(method, kwargs)
    
    return kwargs

def _filter_date_time(start_date: str, end_date: str, kwargs: dict) -> None:
    if start_date and end_date:
        kwargs["date_time__range"] = (
            str_date_to_datetime(start_date), str_date_to_datetime(end_date),
        )
    elif start_date:
        kwargs["date_time__gte"] = str_date_to_datetime(start_date)
    elif end_date:
        kwargs["date_time__lte"] = str_date_to_datetime(end_date)

def _filter_method(method: str, kwargs: dict) -> None:
    if method:
        kwargs["method"] = method