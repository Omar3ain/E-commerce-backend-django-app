from django.urls import include, path
from .views import CreateOrder
urlpatterns = [
  path('', CreateOrder.as_view()),
  path('payments/', include('payments.urls'))
]