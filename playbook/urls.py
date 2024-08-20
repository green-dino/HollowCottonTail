# playbook/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.playbook_view, name='playbook_view'),
]
