"""
Vues pour le module accounts. Ces vues gèrent l'authentification de l'administrateur et les opérations associées.
"""
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Administrateur
from .serializers import ConnexionSerializer, AdministrateurSerializer, AdministrateurConnexionSerializer


class ConnexionView(APIView):
    """
    Vue pour la connexion de l'administrateur.
    Utilise l'authentification par session Django.
    CSRF automatiquement désactivé pour toutes les APIs via middleware.
    """
    permission_classes = [AllowAny]
    serializer_class = ConnexionSerializer
    
    @extend_schema(
        request=ConnexionSerializer,
        responses={
            200: OpenApiResponse(description="Connexion réussie"),
            400: OpenApiResponse(description="Identifiants invalides")
        },
        description="Connexion de l'administrateur",
        operation_id="admin_login"
    )
    def post(self, request, *args, **kwargs):
        """
        Authentifie l'administrateur avec les identifiants fournis.
        """
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Connexion de l'utilisateur avec une session
        user = serializer.validated_data['user']
        login(request, user)
          # Récupérer les informations de l'administrateur
        admin = Administrateur.objects.filter(utilisateurs=user).first()
        
        # Vérifier si l'utilisateur est un administrateur
        if admin is None:
            return Response({
                'message': 'Connexion réussie, mais l\'utilisateur n\'est pas un administrateur',
                'admin': None
            }, status=status.HTTP_200_OK)
            
        # Utiliser le serializer optimisé pour la connexion
        admin_serializer = AdministrateurConnexionSerializer(admin, context={'request': request})
        
        return Response({
            'message': 'Connexion réussie',
            'admin': admin_serializer.data
        }, status=status.HTTP_200_OK)


class DeconnexionView(APIView):
    """
    Vue pour la déconnexion de l'administrateur.
    CSRF automatiquement désactivé pour toutes les APIs via middleware.
    """
    permission_classes = [IsAuthenticated]
    # Définir un serializer pour éviter l'avertissement DRF-Spectacular
    serializer_class = None

    @extend_schema(
        request=None,  # Pas de données d'entrée nécessaires
        responses={
            200: {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Déconnexion réussie"}
                }
            }
        },
        description="Déconnexion de l'administrateur",
        operation_id="admin_logout"
    )
    def post(self, request, *args, **kwargs):
        """
        Déconnecte l'administrateur.
        """
        logout(request)
        return Response({'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)


class ProfileAdminView(generics.RetrieveAPIView):
    """
    Vue pour afficher le profil de l'administrateur connecté.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AdministrateurSerializer
    
    @extend_schema(
        responses={
            200: AdministrateurSerializer,
            403: OpenApiResponse(description="Non autorisé")
        },
        description="Profil de l'administrateur connecté",
        operation_id="admin_profile"
    )
    def get(self, request, *args, **kwargs):
        """
        Récupère les informations de l'administrateur connecté.
        """
        admin = Administrateur.objects.filter(utilisateurs=request.user).first()
        if admin is None:
            return Response(
                {'message': "Vous n'êtes pas un administrateur."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.serializer_class(admin)
        return Response(serializer.data)
