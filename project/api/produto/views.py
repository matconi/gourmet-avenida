from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from rest_framework import status
from api.produto.serializers import UnitsSerializer, ProductVariationsSerializer, ShowcaseSerializer
from api.produto.domain.repositories import unit_repository
from produto.models import Unit
from produto.domain.services import unit_service

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
    offset = int(request.GET.get('offset', 0))
    kwargs = unit_service.filter_units(request)

    units = unit_repository.get_index(kwargs)[offset:offset + unit_repository.CARDS_PER_VIEW]

    serializer = ShowcaseSerializer(units, many=True)
    response_data = {
        "added_units": len(serializer.data),
        "units": serializer.data
    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@login_required
def load_more_category(request, category_slug):
    offset = int(request.GET.get('offset', 0))
    kwargs = unit_service.filter_units(request)

    units = unit_repository.get_index_category(category_slug, kwargs)[offset:offset + unit_repository.CARDS_PER_VIEW]

    serializer = ShowcaseSerializer(units, many=True)
    response_data = {
        "added_units": len(serializer.data),
        "units": serializer.data
    }
    
    return Response(response_data, status=status.HTTP_200_OK)
