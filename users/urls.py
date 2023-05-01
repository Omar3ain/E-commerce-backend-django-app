from django.urls import include, path
from .views import CreateUserView, GetUserView, ListUsersView, DeleteUserView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', ListUsersView.as_view(), name='list_users'),
    path('<int:user_id>/', GetUserView.as_view(), name='get_user'),
    path('delete/<int:user_id>/', DeleteUserView.as_view(), name='delete_user'),
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('login/', obtain_auth_token, name='login'),
    path('cart/', include('cart.urls')),
    path('order/', include('order.urls')),
    path('wishlist/', include('wishlist.urls')),
]