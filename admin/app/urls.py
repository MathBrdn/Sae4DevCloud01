from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('demande/accepter/<int:demande_id>/', views.accepter_demande),
    path('demande/refuser/<int:demande_id>/', views.refuser_demande),
    path('operation/accepter/<int:demande_id>/', views.accepter_operation),
    path('operation/refuser/<int:demande_id>/', views.refuser_operation),
]