# serializers.py
from rest_framework import serializers
from .models import Product
from wishlist.models import Wishlist
class ProductSerializer(serializers.ModelSerializer):
    inWishList = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'

    def get_inWishList(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return Wishlist.objects.filter(product=obj.id, user_id = request.user.id).exists()
        else:
            return False  
