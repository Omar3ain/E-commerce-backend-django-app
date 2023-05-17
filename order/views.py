from .serializers import OrderSerializer, OrderItemSerializer, AddressSerializer
from .models import Order,OrderItem
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ecommerce.permission import IsOwnerOrReadOnly
from django.db import transaction
from cart.models import Cart, CartItem
from products.models import Product
from payments.models import Payment
import logging
from django.db.models import Prefetch

class HandleOrder(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = AddressSerializer
    
    def get(self, request):
        self.check_object_permissions(request, request.user)
        try:
            orders = Order.objects.filter(user_id=request.user.id).order_by('-createdAt')
            orderRes = OrderSerializer(orders, many=True)

            return Response({"order":orderRes.data})
        except Order.DoesNotExist:
            return Response({"error":"order doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        self.check_object_permissions(request, request.user)
        address_serializer = AddressSerializer(data=request.data)
        if address_serializer.is_valid():
            try:
                cart = Cart.objects.get(user_id=request.user.id)
            except Cart.DoesNotExist:
                return Response({"error":"cart doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
            
            cartItems = CartItem.objects.filter(cart_id=cart.id)
            total_amount = 0
            orderID=0
            with transaction.atomic():
    
                order = Order.objects.create(user_id=request.user, total_amount=0)
                order.street_name = address_serializer.data['street_name']
                order.city = address_serializer.data['city']
                order.country = address_serializer.data['country']
                order.building_no = address_serializer.data['building_no']
                order.floor_no = address_serializer.data['floor_no']
                order.apartment_no = address_serializer.data['apartment_no']
                order.save()
                for item in cartItems:  
                    if item.product_id.quantity >= item.quantity:
                        product = Product.objects.get(id=item.product_id.id)
                        product.quantity -= item.quantity
                        product.save()
                    else:
                        return Response({"error": 'product out of stock'}, status=status.HTTP_400_BAD_REQUEST)
    
                    total_amount += item.product_id.price * item.quantity
                    OrderItem.objects.create(order=order, product=item.product_id, quantity=item.quantity)
    
                order.total_amount = total_amount
                order.save()
                cart.delete()
                orderID=order.id
            
            try:
                CreatedOrder = Order.objects.get(id=orderID)
                orderRes = OrderSerializer(CreatedOrder)
                orderItems = OrderItem.objects.filter(order=order.id)
                orderItemsRes = OrderItemSerializer(orderItems, many=True)
                return Response({"order": orderRes.data, "order_items": orderItemsRes.data})
            except Order.DoesNotExist:
                return Response({"error": 'order not found'}, status=status.HTTP_404_NOT_FOUND)
            except OrderItem.DoesNotExist:
                return Response({"error": 'order item not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FindOrder(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self,request,orderId):
        self.check_object_permissions(request, request.user)
        try:
            orderItems = OrderItem.objects.filter(order=orderId)
            orderItemsRes = OrderItemSerializer(orderItems, many=True)
            return Response({"order":orderItemsRes.data})
        except OrderItem.DoesNotExist:
            return Response({"error":"order doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, orderId):
        self.check_object_permissions(request, request.user)
        orderExists = Payment.objects.filter(order=orderId, status = 'requires_payment_method').exists()
        if orderExists:
            try:
                order = Order.objects.filter(id=orderId).first()
                orderItems = OrderItem.objects.filter(order=orderId)
                for item in orderItems:
                    product = Product.objects.get(id=item.product.id)
                    product.quantity += item.quantity
                    product.save()
                order.delete()
                return Response({'orderId':orderId, 'success':'order canceled'}) 
            except OrderItem.DoesNotExist:
                return Response({"error": 'order item not found'}, status=status.HTTP_404_NOT_FOUND)
            except Order.DoesNotExist:
                return Response({"error": 'order not found'}, status=status.HTTP_404_NOT_FOUND)
            except Product.DoesNotExist:
                return Response({"error": 'product not found'}, status=status.HTTP_404_NOT_FOUND)
                # except Exception as e:
                #     return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Can't cancel this order"}, status=status.HTTP_400_BAD_REQUEST)
