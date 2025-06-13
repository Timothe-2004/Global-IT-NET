from django.urls import path
from .views import (
    EmployeListView,
    EmployeDetailView,
    EmployeCreateView,
    EmployeUpdateView,
    EmployeDeleteView,
)

app_name = 'equipe'

urlpatterns = [
    # API de liste des employés
    path('', EmployeListView.as_view(), name='employe-list'),
    
    # API de détail d'un employé
    path('<int:pk>/', EmployeDetailView.as_view(), name='employe-detail'),
    
    # API d'ajout d'un employé (admin uniquement)
    path('create/', EmployeCreateView.as_view(), name='employe-create'),
    
    # API de mise à jour d'un employé (admin uniquement)
    path('<int:pk>/update/', EmployeUpdateView.as_view(), name='employe-update'),
    
    # API de suppression d'un employé (admin uniquement)
    path('<int:pk>/delete/', EmployeDeleteView.as_view(), name='employe-delete'),
]
