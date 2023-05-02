from django.urls import path

from category.views import GetAllCategories

urlpatterns = [
    path('' ,GetAllCategories.as_view() , name="get_all_categories")
]