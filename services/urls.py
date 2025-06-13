from django.urls import path
from .views import (
    ServiceListView,
    ServiceDetailView,
    ServiceCreateView,
    ServiceUpdateView,
    ServiceDeleteView,
)

app_name = 'services'

urlpatterns = [
    # API de liste des services
    path('', ServiceListView.as_view(), name='service-list'),
    
    # API de détail d'un service
    path('<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    
    # API de création d'un service (admin uniquement)
    path('create/', ServiceCreateView.as_view(), name='service-create'),
    
    # API de mise à jour d'un service (admin uniquement)
    path('<int:pk>/update/', ServiceUpdateView.as_view(), name='service-update'),
    
    # API de suppression d'un service (admin uniquement)
    path('<int:pk>/delete/', ServiceDeleteView.as_view(), name='service-delete'),
]
