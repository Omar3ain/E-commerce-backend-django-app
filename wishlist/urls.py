from django.urls import path
from .views import WishlistView, WishlistItemView, addProduct
urlpatterns = [
    path('', WishlistView.as_view()),
    path('add/<int:product_id>', addProduct.as_view()),
    path('<int:pk>', WishlistItemView.as_view())
]