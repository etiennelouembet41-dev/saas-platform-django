from django.urls import path
from . import views

urlpatterns = [
    
    path("", views.clients_list, name="clients_list"),
    path("create/", views.client_create, name="client_create"),
    path("edit/<int:id>/", views.client_edit, name="client_edit"),
    path("delete/<int:id>", views.client_delete, name="client_delete"),
]
