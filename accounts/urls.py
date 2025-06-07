"""
Configuration des URLs pour le module accounts.
Ce module définit les points d'accès API pour l'authentification de l'administrateur.
"""
from django.urls import path
from .views import ConnexionView, DeconnexionView

app_name = 'accounts'

urlpatterns = [
    path('admin/connexion/', ConnexionView.as_view(), name='admin-connexion'),
    path('admin/deconnexion/', DeconnexionView.as_view(), name='admin-deconnexion'),
]