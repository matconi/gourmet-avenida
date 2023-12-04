from rest_framework import serializers
from produto.models import Unit
from api.produto.serializers import UnitsSerializer, ShowcaseSerializer

class UnitsSerializer(UnitsSerializer):
    pass

class FavoritesSerializer(ShowcaseSerializer):
    pass