from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Utilisateur, Inscription, RechercheFormation
from .serializers import (
    UserSerializer, 
    UtilisateurSerializer, 
    InscriptionSerializer,
    RechercheFormationSerializer,
    FormationExterneSerializer
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError, APIException
import logging

logger = logging.getLogger(__name__)

class APIError(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Service temporairement indisponible.'
    default_code = 'service_unavailable'

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Créer un nouveau compte utilisateur",
        request_body=UtilisateurSerializer,
        responses={
            201: openapi.Response('Utilisateur créé avec succès', UtilisateurSerializer),
            400: 'Données invalides'
        }
    )
    def post(self, request):
        try:
            serializer = UtilisateurSerializer(data=request.data)
            if serializer.is_valid():
                utilisateur = serializer.save()
                refresh = RefreshToken.for_user(utilisateur.user)
                return Response({
                    'user': serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Erreur lors de l'inscription: {str(e)}")
            return Response(
                {'error': 'Une erreur est survenue lors de l\'inscription'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Se connecter avec un compte existant",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: openapi.Response('Connexion réussie', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    'access': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )),
            401: 'Identifiants invalides'
        }
    )
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            
            if not username or not password:
                return Response(
                    {'error': 'Username et password requis'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user = authenticate(username=username, password=password)
            
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response(
                {'error': 'Identifiants invalides'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            logger.error(f"Erreur lors de la connexion: {str(e)}")
            return Response(
                {'error': 'Une erreur est survenue lors de la connexion'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RechercheFormationView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Rechercher une formation",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['terme_recherche'],
            properties={
                'terme_recherche': openapi.Schema(type=openapi.TYPE_STRING),
            }
        ),
        responses={
            200: FormationExterneSerializer(many=True),
            400: 'Terme de recherche requis',
            503: 'Service de recherche indisponible'
        }
    )
    def post(self, request):
        try:
            terme_recherche = request.data.get('terme_recherche')
            if not terme_recherche:
                return Response(
                    {'error': 'Terme de recherche requis'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Enregistrer la recherche
            RechercheFormation.objects.create(
                utilisateur=request.user.utilisateur,
                terme_recherche=terme_recherche
            )
            
            # Appeler l'API externe
            try:
                response = requests.get(
                    f"{settings.FORMATION_API_URL}/search",
                    params={'q': terme_recherche},
                    headers={'Authorization': f'Bearer {settings.FORMATION_API_KEY}'},
                    timeout=5
                )
                response.raise_for_status()
                formations = response.json()
                
                # Valider les données reçues
                serializer = FormationExterneSerializer(data=formations, many=True)
                if serializer.is_valid():
                    return Response(serializer.data)
                return Response(
                    {'error': 'Données invalides reçues du service externe'},
                    status=status.HTTP_502_BAD_GATEWAY
                )
                
            except requests.RequestException as e:
                logger.error(f"Erreur API externe: {str(e)}")
                raise APIError()
                
        except Exception as e:
            logger.error(f"Erreur lors de la recherche: {str(e)}")
            return Response(
                {'error': 'Une erreur est survenue lors de la recherche'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class InscriptionView(generics.CreateAPIView):
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="S'inscrire à une formation",
        request_body=InscriptionSerializer,
        responses={
            201: InscriptionSerializer,
            400: 'Données invalides'
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            data['utilisateur'] = request.user.utilisateur.id
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Erreur lors de l'inscription à la formation: {str(e)}")
            return Response(
                {'error': 'Une erreur est survenue lors de l\'inscription à la formation'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user.utilisateur)

class VerificationStatutInscriptionView(generics.RetrieveAPIView):
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Vérifier le statut d'une inscription",
        responses={
            200: InscriptionSerializer,
            404: 'Inscription non trouvée'
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        return Inscription.objects.filter(utilisateur=self.request.user.utilisateur).first()
