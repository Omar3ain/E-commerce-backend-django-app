from django.urls import include, path
from .views import HandleOrder
urlpatterns = [
  path('', HandleOrder.as_view()),
  path('<int:orderId>', HandleOrder.as_view()),
  path('payment/', include('payments.urls'))
] 