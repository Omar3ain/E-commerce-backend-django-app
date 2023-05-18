from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product
from rest_framework.pagination import PageNumberPagination

class getProducts(APIView):
    pagination_class = PageNumberPagination
    def get(self, request):       
        search_param = request.query_params.get('search')
        if search_param:
            products = Product.objects.filter(name__icontains=search_param)
        else:
            products = Product.objects.all().order_by('id')
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
class GetProductById(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data)
class GetProductsByCategoryId(APIView):
    pagination_class = PageNumberPagination
    def get(self, request, category_id):
        search_param = request.query_params.get('search')
        try:
            if search_param:
                products = Product.objects.filter(name__icontains=search_param , category__id=category_id)
            else:
                products = Product.objects.filter(category__id=category_id).order_by('id')
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)