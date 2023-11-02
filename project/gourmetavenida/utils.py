from django.core.paginator import Paginator

def paginate(request, queryset, intens_per_page=10):
    paginator = Paginator(queryset, intens_per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)