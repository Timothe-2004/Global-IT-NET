from django.shortcuts import render
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from backend.permissions import IsAdminUser, IsAdminOrReadOnly, IsAdminOrCreateOnly
from .models import OffreStage, DemandeStage
from .serializers import DemandeStageSerializer, OffreStageSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(summary="Lister les offres de stage"),
    retrieve=extend_schema(summary="Voir une offre de stage"),
    create=extend_schema(summary="Créer une offre de stage"),
    update=extend_schema(summary="Mettre à jour une offre de stage"),
    partial_update=extend_schema(summary="Mise à jour partielle d'une offre de stage"),
    destroy=extend_schema(summary="Supprimer une offre de stage"),
)
class OffreStageViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les offres de stage.
    - READ (list, retrieve): Public (AllowAny)
    - CREATE/UPDATE/DELETE: Admin uniquement
    """
    queryset = OffreStage.objects.all()
    serializer_class = OffreStageSerializer
    permission_classes = [IsAdminOrReadOnly]

@extend_schema_view(
    list=extend_schema(summary="Lister les demandes de stage"),
    retrieve=extend_schema(summary="Voir une demande de stage"),
    create=extend_schema(summary="Créer une demande de stage"),
    update=extend_schema(summary="Mettre à jour une demande de stage"),
    partial_update=extend_schema(summary="Mise à jour partielle d'une demande de stage"),
    destroy=extend_schema(summary="Supprimer une demande de stage"),
)
class DemandeStageViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour les demandes de stage.
    - CREATE: Public (AllowAny) - permet aux candidats de postuler
    - READ/UPDATE/DELETE: Admin uniquement
    """
    queryset = DemandeStage.objects.all()
    serializer_class = DemandeStageSerializer
    permission_classes = [IsAdminOrCreateOnly]

    def get_queryset(self):
        """
        Retourne toutes les demandes si l'utilisateur est admin,
        sinon aucune demande (sécurité).
        """
        if self.request.user.is_authenticated:
            try:
                from accounts.models import Administrateur
                if Administrateur.objects.filter(utilisateurs=self.request.user).exists():
                    return DemandeStage.objects.all()
            except Exception:
                pass
        return DemandeStage.objects.none()

    @extend_schema(summary="Mettre à jour le statut d'une demande")
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        if not request.user.is_staff:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        demande = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(DemandeStage.STATUT_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        demande.statut = new_status
        demande.save()
        serializer = self.get_serializer(demande)
        return Response(serializer.data)
