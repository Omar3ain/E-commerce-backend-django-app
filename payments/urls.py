from django.urls import path
from .views import CreatePayment,CancelPayment

urlpatterns = [
    path('<int:orderId>/', CreatePayment.as_view()),
    path('<int:orderId>/cancel', CancelPayment.as_view()),
]