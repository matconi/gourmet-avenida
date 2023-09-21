from rest_framework import routers, serializers, viewsets
from produto.models.Unit import Unit

class ProductVariationsSerializer(serializers.Serializer):
    def to_representation(self, instance):
        representation = super(ProductVariationsSerializer, self).to_representation(instance)
        return {
            "variants": [
                {
                    "id": variant['variations__variant__id'],
                    "name": variant['variations__variant__name'],
                    "variations": [
                        {
                            "id": variation['variations__id'],
                            "name": variation['variations__name']
                        } 
                        
                        for variation in instance 
                            if variation['variations__variant__id'] == variant['variations__variant__id']
                    ]
                } 
                
                for variant in instance
            ],
        }

class UnitsSerializer(serializers.ModelSerializer):
    variations = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Unit
        fields = ['id', 'name', 'image', 'price', 'promotional', 'variations']