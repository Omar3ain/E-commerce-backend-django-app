from rest_framework import serializers
from .models import  Order, OrderItem

class orderSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Order
        fields = '__all__'

        
class orderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model =  OrderItem
        fields = '__all__'
