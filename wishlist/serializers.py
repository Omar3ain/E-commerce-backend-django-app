from rest_framework import serializers
from .models import  Wishlist

class wishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Wishlist
        fields = '__all__'