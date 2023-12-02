from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import status
from .serializers import FavoritesSerializer
from produto.domain.repositories import unit_repository
from produto.models import Unit
from produto.domain.services import unit_service


@api_view(['GET'])
@login_required
@permission_required('usuario.favorites')
def load_more_favorites(request):
    offset = int(request.GET.get('offset', 0))
    
    kwargs = unit_service.filter_units(request)

    units = unit_repository.get_customer_favorites(request.user.user_customer, kwargs)[offset:offset + unit_repository.CARDS_PER_VIEW]

    serializer = FavoritesSerializer(units, many=True)
    response_data = {
        "added_units": len(serializer.data),
        "units": serializer.data
    }

    return Response(response_data, status=status.HTTP_200_OK)