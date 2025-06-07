from django.urls import path
from .views import (
    PartenaireListCreateView,
    PartenaireRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('partenaire', PartenaireListCreateView.as_view(), name='partenaire-list-create'),
    path('<int:pk>/partenaire-update', PartenaireRetrieveUpdateDestroyView.as_view(), name='partenaire-detail'),
]
