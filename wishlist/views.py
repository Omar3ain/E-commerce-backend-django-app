from .serializers import wishlistSerializer
from .models import Wishlist
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ecommerce.permission import IsOwnerOrReadOnly
from products.models import Product
# Create your views here.

class WishlistView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request):
        user = request.user
        self.check_object_permissions(request, user)

        wish_list = Wishlist.objects.filter(user_id=user.id)
        serializer = wishlistSerializer(wish_list, many=True)
        return Response({"wishlist":serializer.data})

class addProduct(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request, product_id):
        self.check_object_permissions(request, request.user)
        try:
            Product.objects.get(id=product_id)
        except:
            return Response({"error":"product doesn't exist"}, status=status.HTTP_404_NOT_FOUND)
        
        product_exists = Wishlist.objects.filter(product=product_id, user_id=request.user.id).first()

        if product_exists:
            return Response({"error":"already in wishlist"}, status=status.HTTP_404_NOT_FOUND)

        else:
            request.data['user_id'] = request.user.id
            request.data['product'] =product_id
            serializer = wishlistSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            



class WishlistItemView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
  
    def get(self, request, pk):
        try: 
            user = request.user
            self.check_object_permissions(request, user)
            wish_list= Wishlist.objects.get(user_id=user.id, product_id=pk)
            serializer = wishlistSerializer(wish_list)
            return Response({"wishlist":serializer.data})    
        except:
            return Response({'error':'item does not exist'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try: 
            user = request.user
            self.check_object_permissions(request, user)
            wish_list= Wishlist.objects.get(user_id=user.id, product_id=pk)
            serializer = wishlistSerializer(wish_list)
            wish_list.delete() 
            return Response(serializer.data) 
        except:
            return Response({'error':'item does not exist'}, status=status.HTTP_404_NOT_FOUND)

