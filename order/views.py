from .serializers import orderSerializer, orderItemSerializer
from .models import Order,OrderItem
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ecommerce.permission import IsOwnerOrReadOnly
from django.db import transaction
from cart.models import Cart, CartItem


class CreateOrder(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    # def calculate_total_amount(self):
    def post(self, request):
        self.check_object_permissions(request, request.user)
        try:
            cart = Cart.objects.get(user_id=request.user.id)
        except:
            return Response({"error":"cart doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        cartItems = CartItem.objects.filter(cart_id=cart.id)
        total_amount = 0
        with transaction.atomic():
            order = Order.objects.create(user_id=request.user.id, total_amount=0)
            
            for item in cartItems:
                total_amount += item.product_id.price * item.quantity
                OrderItem.objects.create(order=order, product=item.product_id, quantity=item.quantity)

            order.total_amount = total_amount
            order.save()
            cart.delete()
            
        orderItems = OrderItem.objects.filter(order=order.id)
        orderItemsRes = orderItemSerializer(data=orderItems)
        orderRes = orderSerializer(data=order)
        return Response({"order": orderRes, "order_items": orderItemsRes})