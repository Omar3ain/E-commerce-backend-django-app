from rest_framework import serializers
from .models import  Order, OrderItem
from django_countries.serializer_fields import CountryField
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Order
        fields = '__all__'
        
class AddressSerializer(serializers.Serializer):
    country = CountryField()
    street_name = serializers.CharField(max_length=255)
    building_no = serializers.IntegerField()
    floor_no = serializers.IntegerField()
    apartment_no = serializers.IntegerField()
    
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model =  OrderItem
        fields = '__all__'
