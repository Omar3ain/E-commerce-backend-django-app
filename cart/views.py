from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ecommerce.permission import IsOwnerOrReadOnly
from rest_framework.views import APIView
from .models import Cart, CartItem
from .serializers import CartItemSerializer
from users.models import User
from products.models import Product
# Create your views here.

class CartCreateView(APIView):
    
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    # def decreaseProduct(self, product):
    #     product.quantity -= 1
    #     product.save()
        
    def post(self, request, product_id):
        user = request.user
        product = Product.objects.get(id=product_id)
        if product:
            if product.quantity > 0:
                self.check_object_permissions(request, user)
                cart = Cart.objects.filter(user_id=user).first()
                if cart:
                    cart_item = CartItem.objects.filter(product_id=product_id, cart_id=cart).first()
                    if cart_item:
                        cart_item.quantity += 1
                        cart_item.save()
                        # self.decreaseProduct(product)
                        serializer = CartItemSerializer(cart_item)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        cart_item = CartItem.objects.create(product_id=product, cart_id=cart, quantity=1)
                        # self.decreaseProduct(product)
                        serializer = CartItemSerializer(cart_item)
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    cart = Cart.objects.create(user_id=request.user)
                    cart_item = CartItem.objects.create(product_id=product, cart_id=cart, quantity=1)
                    # self.decreaseProduct(product)
                    serializer = CartItemSerializer(cart_item)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error" : "Out of Stock"})
        else:
            return Response({"error" : "Product not found"})
            
        
    

class GetCart(APIView):
    
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    def get(self, request):
        self.check_object_permissions(request, request.user)
        try:
            cart = Cart.objects.get(user_id = request.user.id)
            cartitems = CartItem.objects.filter(cart_id=cart.id)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart Itemss not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartItemSerializer(cartitems, many=True)
        return Response({"Cart": serializer.data})


class DeleteCartItem(APIView):
    
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    
    # def increaseProduct(self, product):
    #     product.quantity += 1
    #     product.save()
    
    def delete(self, request, cartitem):
        try:
            self.check_object_permissions(request, request.user)
            cart = Cart.objects.get(user_id=request.user.id)
            cartItem = CartItem.objects.get(cart_id=cart.id, id=cartitem)
            if cartItem.quantity > 0:
                cartItem.quantity -= 1
                cartItem.save()
                if cartItem.quantity == 0:
                    cartItem.delete()
                # product = Product.objects.get(id=cartItem.product_id.id)
                # if product:
                #     self.increaseProduct(product)
                return Response(status=status.HTTP_204_NO_CONTENT)
            elif cartItem.quantity < 0:
                return Response({"error": "Invalid quantity for cart item"}, status=status.HTTP_400_BAD_REQUEST)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"error": "internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)