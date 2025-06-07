from django.shortcuts import render
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
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
    queryset = OffreStage.objects.all()
    serializer_class = OffreStageSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

@extend_schema_view(
    list=extend_schema(summary="Lister les demandes de stage"),
    retrieve=extend_schema(summary="Voir une demande de stage"),
    create=extend_schema(summary="Créer une demande de stage"),
    update=extend_schema(summary="Mettre à jour une demande de stage"),
    partial_update=extend_schema(summary="Mise à jour partielle d'une demande de stage"),
    destroy=extend_schema(summary="Supprimer une demande de stage"),
)
class DemandeStageViewSet(viewsets.ModelViewSet):
    queryset = DemandeStage.objects.all()
    serializer_class = DemandeStageSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_staff:
            return DemandeStage.objects.all()
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
