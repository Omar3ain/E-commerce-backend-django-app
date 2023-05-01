from django.urls import include, path

urlpatterns = [
  path('payment/', include('payments.urls')),
]