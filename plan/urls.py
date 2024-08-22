from django.urls import include, path
from .views import index , post_list


urlpatterns = [
    path("", view= index),
    path("list", view=post_list)
]
