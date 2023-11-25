from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import status
from api.produto.serializers import UnitsSerializer, ProductVariationsSerializer, ShowcaseSerializer
from api.produto.domain.repositories import unit_repository
from produto.models import Unit
from gourmetavenida.utils import is_ajax

@api_view(['GET'])
@login_required
def view_product(request, slug):  
    units = unit_repository.get_units_variations(slug)
   
    variations_values = unit_repository.get_variations_values(units)

    units_serializer = UnitsSerializer(units, many=True)
    product_variations_serializer = ProductVariationsSerializer(variations_values)

    response_data = {
        "units": units_serializer.data,
        "summary": product_variations_serializer.data
    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@login_required
def load_more(request):
    if is_ajax(request):  
        offset = int(request.GET.get('offset', 0))
        units = unit_repository.get_index()[offset:offset + unit_repository.CARDS_PER_VIEW]

        serializer = ShowcaseSerializer(units, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response('Header X-Requested-With: XMLHttpRequest required', status=status.HTTP_406_NOT_ACCEPTABLE, content_type='text/html')

@api_view(['GET'])
@login_required
def load_more_category(request, category_slug):
    if is_ajax(request):  
        offset = int(request.GET.get('offset', 0))
        units = unit_repository.get_index_category(category_slug)[offset:offset + unit_repository.CARDS_PER_VIEW]

        serializer = ShowcaseSerializer(units, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response('Header X-Requested-With: XMLHttpRequest required', status=status.HTTP_406_NOT_ACCEPTABLE, content_type='text/html')