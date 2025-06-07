from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from django.db.models import Count
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, extend_schema_view
from backend.permissions import IsAdminUser as CustomIsAdminUser

from .models import Realisation, Categorie
from .serializers import (
    RealisationListSerializer,
    RealisationDetailSerializer,
    RealisationCreateUpdateSerializer
)


class RealisationListView(generics.ListAPIView):
    """
    Vue pour lister toutes les réalisations avec possibilité de filtrer par catégorie.
    """
    serializer_class = RealisationListSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        """
        Filtre les réalisations par catégorie si un paramètre 'categorie' est fourni.
        """
        queryset = Realisation.objects.all()
        categorie = self.request.query_params.get('categorie')
        
        if categorie:
            # Vérifier si la catégorie est valide
            if categorie in dict(Categorie.choices):
                queryset = queryset.filter(categorie=categorie)
        
        return queryset


class RealisationDetailView(generics.RetrieveAPIView):
    """
    Vue pour afficher les détails d'une réalisation spécifique.
    """
    queryset = Realisation.objects.all()
    serializer_class = RealisationDetailSerializer
    permission_classes = [AllowAny]


class RealisationCreateView(generics.CreateAPIView):
    """
    Vue pour créer une nouvelle réalisation.
    Seul l'administrateur peut créer des réalisations.
    """
    serializer_class = RealisationCreateUpdateSerializer
    permission_classes = [CustomIsAdminUser]


class RealisationUpdateView(generics.UpdateAPIView):
    """
    Vue pour mettre à jour une réalisation existante.
    Seul l'administrateur peut mettre à jour des réalisations.
    """
    queryset = Realisation.objects.all()
    serializer_class = RealisationCreateUpdateSerializer
    permission_classes = [CustomIsAdminUser]


class RealisationDeleteView(generics.DestroyAPIView):
    """
    Vue pour supprimer une réalisation.
    Seul l'administrateur peut supprimer des réalisations.
    """
    queryset = Realisation.objects.all()
    permission_classes = [CustomIsAdminUser]


@api_view(['GET'])
@permission_classes([AllowAny])
@extend_schema(
    responses={200: {"type": "object", "properties": {"categories": {"type": "array", "items": {"type": "object", "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "count": {"type": "integer"}
    }}}}}},
    description="Récupère la liste de toutes les catégories avec le nombre de réalisations par catégorie",
    operation_id="list_categories",
    tags=["Catégories"]
)
def liste_categories(request):
    """
    Vue pour récupérer la liste des catégories disponibles et leur nombre de réalisations.
    Cette vue est utilisée pour le système de filtre sur la page des réalisations.
    """
    # Récupère les catégories distinctes qui ont au moins une réalisation
    categories = Realisation.objects.values('categorie').annotate(count=Count('id')).order_by('categorie')
    
    # Prépare la réponse
    formatted_categories = []
    for cat in categories:
        cat_value = cat['categorie']
        cat_name = dict(Categorie.choices).get(cat_value, cat_value)
        formatted_categories.append({
            'id': cat_value,
            'name': cat_name,
            'count': cat['count']
        })
    
    # Ajoute également toutes les catégories possibles même si elles n'ont pas de réalisations
    all_categories = dict(Categorie.choices)
    existing_cats = {cat['id'] for cat in formatted_categories}
    
    for cat_value, cat_name in all_categories.items():
        if cat_value not in existing_cats:
            formatted_categories.append({
                'id': cat_value,
                'name': cat_name,
                'count': 0
            })
    
    return Response({'categories': formatted_categories})
