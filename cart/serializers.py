# serializers.py
from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product_id = ProductSerializer(read_only=True);
    class Meta:
        model = CartItem
        fields = ('id', 'product_id', 'quantity', 'cart_id')