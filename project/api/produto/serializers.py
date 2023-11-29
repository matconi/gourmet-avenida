from rest_framework import serializers
from produto.models import Unit

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
            ]
        }

class UnitsSerializer(serializers.ModelSerializer):
    variations = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

    class Meta:
        model = Unit
        fields = ('id', 'name', 'image_lg', 'price', 'promotional', 'variations',)

class ShowcaseSerializer(serializers.ModelSerializer):
    uid = serializers.SerializerMethodField()
    category_slug = serializers.SerializerMethodField()
    product_slug = serializers.SerializerMethodField()

    def get_uid(self, unit):
        return unit.id
        
    def get_product_slug(self, unit):
        return unit.product.slug

    def get_category_slug(self, unit):
        return unit.product.category.slug

    class Meta:
        model = Unit
        fields = ('uid', 'name', 'image_sm', 'price', 'promotional', 'category_slug', 'product_slug',)