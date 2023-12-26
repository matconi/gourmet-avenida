from django.template import Library
from django.utils.html import format_html
from produto.templatetags.produto_pipe import currencyformat

register = Library()

@register.filter
def get_bill(bill: float) -> str:
    return currencyformat(bill) if bill >= 0 else format_html('{}<small class="fs-6"> (em haver)</small>', currencyformat(abs(bill)))