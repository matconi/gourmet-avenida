from django.core.paginator import Paginator
from datetime import datetime

def paginate(request, queryset, intens_per_page=10):
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