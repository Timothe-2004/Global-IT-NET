from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OffreStageViewSet, DemandeStageViewSet

# Création du routeur
router = DefaultRouter()
router.register(r'offres', OffreStageViewSet)
router.register(r'demandes', DemandeStageViewSet)

# Définition des URLs
urlpatterns = [
    path('', include(router.urls)),
] 