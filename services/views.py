from rest_framework import generics
from rest_framework.permissions import AllowAny
from backend.permissions import IsAdminOrReadOnly
from .models import Service
from .serializers import (
    ServiceSerializer, 
    ServiceListSerializer, 
    ServiceCreateUpdateSerializer
)
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample

@extend_schema_view(
    get=extend_schema(
        summary="Lister tous les services",
        description="Retourne la liste de tous les services proposés par l'entreprise.",
        responses={200: ServiceListSerializer(many=True)}
    )
)
class ServiceListView(generics.ListAPIView):
    """
    Vue pour lister tous les services.
    Accessible à tous (lecture publique).
    """
    queryset = Service.objects.all()
    serializer_class = ServiceListSerializer
    permission_classes = [AllowAny]


@extend_schema_view(
    get=extend_schema(
        summary="Détails d'un service",
        description="Retourne les détails complets d'un service spécifique.",
        responses={200: ServiceSerializer}
    )
)
class ServiceDetailView(generics.RetrieveAPIView):
    """
    Vue pour afficher les détails d'un service spécifique.
    Accessible à tous (lecture publique).
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]


@extend_schema_view(
    post=extend_schema(
        summary="Créer un nouveau service",
        description="Crée un nouveau service. Réservé aux administrateurs.",
        request=ServiceCreateUpdateSerializer,
        responses={201: ServiceSerializer},
        examples=[
            OpenApiExample(
                name="Exemple de création de service",
                value={
                    "titre": "Développement Web",
                    "sous_titre": "Solutions web modernes et performantes",
                    "description": "Nous développons des applications web sur mesure utilisant les dernières technologies.",
                    "details": [
                        {
                            "specificite": "Technologies modernes",
                            "detail": "React, Django, Node.js et autres frameworks récents"
                        },
                        {
                            "specificite": "Design responsive",
                            "detail": "Applications adaptées à tous les appareils"
                        },
                        {
                            "specificite": "Performance optimisée",
                            "detail": "Chargement rapide et expérience utilisateur fluide"
                        }
                    ]
                },
                request_only=True
            )
        ]
    )
)
class ServiceCreateView(generics.CreateAPIView):
    """
    Vue pour créer un nouveau service.
    Seul l'administrateur peut créer des services.
    """
    serializer_class = ServiceCreateUpdateSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema_view(
    put=extend_schema(
        summary="Mettre à jour un service",
        description="Met à jour un service existant. Réservé aux administrateurs.",
        request=ServiceCreateUpdateSerializer,
        responses={200: ServiceSerializer}
    ),
    patch=extend_schema(
        summary="Mise à jour partielle d'un service",
        description="Met à jour partiellement un service existant. Réservé aux administrateurs.",
        request=ServiceCreateUpdateSerializer,
        responses={200: ServiceSerializer}
    )
)
class ServiceUpdateView(generics.UpdateAPIView):
    """
    Vue pour mettre à jour un service existant.
    Seul l'administrateur peut mettre à jour des services.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceCreateUpdateSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema_view(
    delete=extend_schema(
        summary="Supprimer un service",
        description="Supprime un service existant. Réservé aux administrateurs.",
        responses={204: None}
    )
)
class ServiceDeleteView(generics.DestroyAPIView):
    """
    Vue pour supprimer un service.
    Seul l'administrateur peut supprimer des services.
    """
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminOrReadOnly]
