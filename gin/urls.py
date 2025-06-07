from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import FormationViewSet,InscriptionFormationViewSet


app_name = 'formations'

#On crée un objet router
router =DefaultRouter()
#On enregistre les viewsets avec une url racine 
router.register(r"formations",FormationViewSet)
router.register(r"inscriptions",InscriptionFormationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
