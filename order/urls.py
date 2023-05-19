from django.urls import include, path
from .views import HandleOrder, FindOrder
urlpatterns = [
  path('', HandleOrder.as_view()),
  path('<int:orderId>', FindOrder.as_view()),
  path('payment/', include('payments.urls'))
] 