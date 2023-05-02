from .serializers import OrderSerializer, OrderItemSerializer
from .models import Order,OrderItem
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ecommerce.permission import IsOwnerOrReadOnly
from django.db import transaction
from cart.models import Cart, CartItem
from products.models import Product


class CreateOrder(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def post(self, request):
        self.check_object_permissions(request, request.user)
        try:
            cart = Cart.objects.get(user_id=request.user.id)
        except:
            return Response({"error":"cart doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        cartItems = CartItem.objects.filter(cart_id=cart.id)
        total_amount = 0
        orderID=0
        with transaction.atomic():

            order = Order.objects.create(user_id=request.user, total_amount=0)           
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

        
    

#cancel order before payment
##cancel order => free, paid
#return payment - fee