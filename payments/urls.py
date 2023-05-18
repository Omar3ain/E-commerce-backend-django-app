from django.urls import path
from .views import CreatePayment,CancelPayment, UpdatePayment, ContinuePayment

urlpatterns = [
    path('<int:orderId>/', CreatePayment.as_view()),
    path('<int:orderId>/cancel', CancelPayment.as_view()),
    path('<int:orderId>/update', UpdatePayment.as_view()),
    path('<int:orderId>/continue', ContinuePayment.as_view()),
]