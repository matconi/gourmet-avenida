from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.produto.serializers import UnitsSerializer, ProductVariationsSerializer
from api.produto.domain.repositories import unit_repository

@api_view(['GET'])
def view_product(request, slug):  
    units = unit_repository.get_units_variations(slug)
   
    variations_values = unit_repository.get_variations_values(units)

    units_serializer = UnitsSerializer(units, many=True)
    product_variations_serializer = ProductVariationsSerializer(variations_values)

    response_data = {
        "units": units_serializer.data,
        "summary": product_variations_serializer.data
    }

    return Response(response_data, status=200)
