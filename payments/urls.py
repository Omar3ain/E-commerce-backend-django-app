from django.urls import path
from .views import CreatePayment

urlpatterns = [
    path('<int:orderId>/', CreatePayment.as_view()),
]