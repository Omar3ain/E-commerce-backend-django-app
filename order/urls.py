from django.urls import include, path
from .views import CreateOrder
urlpatterns = [
  path('payment/', include('payments.urls')),
  path('', CreateOrder.as_view()),
]