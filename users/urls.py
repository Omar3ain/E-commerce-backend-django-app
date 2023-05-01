from django.urls import include, path
from .views import CreateUserView, LoginView

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('wishlist/', include('wishlist.urls')),
]