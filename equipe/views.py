from rest_framework import generics
from rest_framework.permissions import AllowAny
from backend.permissions import IsAdminOrReadOnly
from .models import Employe
from .serializers import (
    EmployeSerializer, 
    EmployeListSerializer, 
    EmployeCreateUpdateSerializer
)
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample

@extend_schema_view(
    get=extend_schema(
        summary="Lister tous les employés",
        description="Retourne la liste de tous les membres de l'équipe.",
        responses={200: EmployeListSerializer(many=True)}
    )
)
class EmployeListView(generics.ListAPIView):
    """
    Vue pour lister tous les employés.
    Accessible à tous (lecture publique).
    Par défaut, seuls les employés actifs sont affichés.
    """
    serializer_class = EmployeListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """Retourne les employés actifs par défaut."""
        queryset = Employe.objects.filter(actif=True)
        # Permettre de voir tous les employés avec un paramètre
        show_all = self.request.query_params.get('tous', None)
        if show_all and show_all.lower() in ['true', '1']:
            queryset = Employe.objects.all()
        return queryset


@extend_schema_view(
    get=extend_schema(
        summary="Détails d'un employé",
        description="Retourne les détails complets d'un membre de l'équipe.",
        responses={200: EmployeSerializer}
    )
)
class EmployeDetailView(generics.RetrieveAPIView):
    """
    Vue pour afficher les détails d'un employé spécifique.
    Accessible à tous (lecture publique).
    """
    queryset = Employe.objects.all()
    serializer_class = EmployeSerializer
    permission_classes = [AllowAny]


@extend_schema_view(
    post=extend_schema(
        summary="Ajouter un nouvel employé",
        description="Ajoute un nouveau membre à l'équipe. Réservé aux administrateurs.",
        request=EmployeCreateUpdateSerializer,
        responses={201: EmployeSerializer},
        examples=[
            OpenApiExample(
                name="Exemple d'ajout d'employé",                value={
                    "nom": "Dupont",
                    "prenom": "Jean",
                    "poste": "Développeur Full Stack",
                    "actif": True
                },
                request_only=True
            )
        ]
    )
)
class EmployeCreateView(generics.CreateAPIView):
    """
    Vue pour ajouter un nouveau membre à l'équipe.
    Seul l'administrateur peut ajouter des employés.
    """
    serializer_class = EmployeCreateUpdateSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema_view(
    put=extend_schema(
        summary="Mettre à jour un employé",
        description="Met à jour les informations d'un employé. Réservé aux administrateurs.",
        request=EmployeCreateUpdateSerializer,
        responses={200: EmployeSerializer}
    ),
    patch=extend_schema(
        summary="Mise à jour partielle d'un employé",
        description="Met à jour partiellement les informations d'un employé. Réservé aux administrateurs.",
        request=EmployeCreateUpdateSerializer,
        responses={200: EmployeSerializer}
    )
)
class EmployeUpdateView(generics.UpdateAPIView):
    """
    Vue pour mettre à jour les informations d'un employé.
    Seul l'administrateur peut mettre à jour des employés.
    """
    queryset = Employe.objects.all()
    serializer_class = EmployeCreateUpdateSerializer
    permission_classes = [IsAdminOrReadOnly]


@extend_schema_view(
    delete=extend_schema(
        summary="Supprimer un employé",
        description="Supprime un employé de l'équipe. Réservé aux administrateurs.",
        responses={204: None}
    )
)
class EmployeDeleteView(generics.DestroyAPIView):
    """
    Vue pour supprimer un employé.
    Seul l'administrateur peut supprimer des employés.
    """
    queryset = Employe.objects.all()
    serializer_class = EmployeSerializer
    permission_classes = [IsAdminOrReadOnly]
