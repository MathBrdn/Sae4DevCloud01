from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.index),
    path('<int:user_id>/create/', views.create_compte),
    path('<int:user_id>/compte/<int:id>/', views.affiche_compte),
    path('<int:user_id>/update/<int:compte_id>/', views.update_compte),
    path('<int:user_id>/delete/<int:compte_id>/', views.delete_compte),
]