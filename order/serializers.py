from rest_framework import serializers
from .models import  Order, OrderItem
from django_countries.serializer_fields import CountryField
from products.serializers import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Order
        fields = '__all__'
        
class AddressSerializer(serializers.Serializer):
    country = CountryField()
    city = serializers.CharField(max_length=255)
    street_name = serializers.CharField(max_length=255)
    building_no = serializers.IntegerField()
    floor_no = serializers.IntegerField()
    apartment_no = serializers.IntegerField()
    
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model =  OrderItem
        fields = '__all__'
    def to_representation(self, instance):
        # include product details in representation
        self.fields['product'] = ProductSerializer()
        return super().to_representation(instance)

