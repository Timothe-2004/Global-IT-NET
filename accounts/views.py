"""
Vues pour le module accountsCes vues gèrent l'authentification de l'administrateur et les opérations associées.
"""
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Administrateur
from .serializers import ConnexionSerializer, AdministrateurSerializer


class ConnexionView(APIView):
    """
    Vue pour la connexion de l'administrateur.
    Utilise l'authentification par session Django.
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
        admin = Administrateur.objects.filter(utilisateur=user).first()
        
        # Vérifier si l'utilisateur est un administrateur
        if admin is None:
            return Response({
                'message': 'Connexion réussie, mais l\'utilisateur n\'est pas un administrateur',
                'admin': None
            }, status=status.HTTP_200_OK)
            
        admin_serializer = AdministrateurSerializer(admin)
        
        return Response({
            'message': 'Connexion réussie',
            'admin': admin_serializer.data
        }, status=status.HTTP_200_OK)


class DeconnexionView(APIView):
    """
    Vue pour la déconnexion de l'administrateur.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: OpenApiResponse(description="Déconnexion réussie")},
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
        admin = Administrateur.objects.filter(utilisateur=request.user).first()
        if admin is None:
            return Response(
                {'message': "Vous n'êtes pas un administrateur."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.serializer_class(admin)
        return Response(serializer.data)
