from django.urls import path

from products.views import  getProducts ,GetProductById ,GetProductsByCategoryId

urlpatterns = [
    path('' , getProducts.as_view(), name='get_all_products'),
    path('<int:pk>/', GetProductById.as_view() , name='get_product_by_id'),
    path('<int:category_id>/get/', GetProductsByCategoryId.as_view(),name='get_product_by_category_id'),
]