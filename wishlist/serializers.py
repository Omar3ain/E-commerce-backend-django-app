from rest_framework import serializers
from .models import  Wishlist
from products.serializers import ProductSerializer

class wishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Wishlist
        fields = '__all__'

    def to_representation(self, instance):
        # include product details in representation
        self.fields['product'] = ProductSerializer()
        return super().to_representation(instance)
