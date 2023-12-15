from rest_framework import serializers
from produto.models import Unit

class ProductVariationsSerializer(serializers.Serializer):
    def to_representation(self, instance):
        representation = super(ProductVariationsSerializer, self).to_representation(instance)
        return {
            "varieties": [
                {
                    "id": variety['variations__variety__id'],
                    "name": variety['variations__variety__name'],
                    "variations": [
                        {
                            "id": variation['variations__id'],
                            "name": variation['variations__name']
                        } 
                        
                        for variation in instance 
                            if variation['variations__variety__id'] == variety['variations__variety__id']
                    ]
                } 
                
                for variety in instance
            ]
        }

class UnitsSerializer(serializers.ModelSerializer):
    variations = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    is_favorite = serializers.SerializerMethodField()

    def get_is_favorite(self, unit: Unit):
        return True if unit.unit_favorite.all() else False

    class Meta:
        model = Unit
        fields = ('id', 'name', 'image_lg', 'price', 'promotional', 'stock', 'booked', 'variations', 'is_favorite',)

class ShowcaseSerializer(serializers.ModelSerializer):
    uid = serializers.SerializerMethodField()
    avaliable = serializers.SerializerMethodField()
    category_slug = serializers.SerializerMethodField()
    product_slug = serializers.SerializerMethodField()

    def get_uid(self, unit: Unit):
        return unit.id
        
    def get_avaliable(self, unit: Unit):
        return unit.avaliable()
        
    def get_category_slug(self, unit: Unit):
        return unit.product.category.slug

    def get_product_slug(self, unit: Unit):
        return unit.product.slug

    class Meta:
        model = Unit
        fields = ('uid', 'name', 'image_sm', 'price', 'promotional', 'stock', 'avaliable', 'category_slug', 'product_slug',)