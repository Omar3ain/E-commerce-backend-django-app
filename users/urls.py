from django.urls import include, path
from .views import CreateUserView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    # path('login/', LoginView.as_view(), name='login'),
    path('login/', obtain_auth_token, name='login'),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('wishlist/', include('wishlist.urls')),
]