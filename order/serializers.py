from rest_framework import serializers
from .models import  Order, OrderItem
from django_countries.serializer_fields import CountryField
from products.serializers import ProductSerializer
from payments.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('status', 'amount', 'currency')
class OrderSerializer(serializers.ModelSerializer):
    payment = serializers.SerializerMethodField()
    order_details = serializers.SerializerMethodField()
    class Meta:
        model =  Order
        fields = '__all__'
    def get_payment(self, order):
        try:
            payment = Payment.objects.get(order=order)
            return PaymentSerializer(payment).data
        except:
            pass
    def get_order_details(self, order):
        order_items = OrderItem.objects.filter(order=order)
        order_item_serializer = OrderItemSerializer(order_items, many=True)
        return order_item_serializer.data
        

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

