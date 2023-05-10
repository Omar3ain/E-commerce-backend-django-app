from django.urls import path
from .views import CartCreateView, GetCart, DeleteCartItem, AddQuantity

urlpatterns = [
       path('', GetCart.as_view(), name='cart-detail'),
       path('<int:product_id>/', CartCreateView.as_view(), name='cart-add'),
       path('delete/<int:cartitem>/', DeleteCartItem.as_view(), name='cartItem-delete'),
       path('add/<int:cartitem>',  AddQuantity.as_view(), name='cartItem-add'),
]