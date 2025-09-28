from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('upload/', views.upload_document, name='upload_document'),
    path('delete/<int:pk>/', views.document_delete, name='document_delete'),

    # Criar kit sem ID
    path('create-kit/', views.create_kit, name='create_kit'),

    # Editar kit com ID
    path('edit-kit/<int:kit_id>/', views.edit_kit, name='edit_kit'),

    # Deletar kit
    path('delete-kit/<int:kit_id>/', views.kit_delete, name='kit_delete'),
]
