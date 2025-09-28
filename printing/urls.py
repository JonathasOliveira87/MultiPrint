from django.urls import path
from . import views

urlpatterns = [
    path('', views.print_documents, name='print_documents'),
]
