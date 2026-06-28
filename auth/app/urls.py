from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('inscription/', views.inscription),
    path('login/', views.login)
]