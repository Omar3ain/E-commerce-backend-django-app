# serializers.py
from rest_framework import serializers
from .models import Product
from wishlist.models import Wishlist
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'