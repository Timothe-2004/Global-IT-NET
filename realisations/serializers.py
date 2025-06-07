from rest_framework import serializers
from .models import Realisation, Categorie

class RealisationListSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour l'affichage de la liste des réalisations.
    Affiche des informations réduites: nom du projet, description, catégorie, et une seule image.
    """
    categorie_display = serializers.CharField(source='get_categorie_display', read_only=True)
    
    class Meta:
        model = Realisation
        fields = ['id', 'nomProjet', 'description', 'categorie', 'categorie_display', 'image1']


class RealisationDetailSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour l'affichage détaillé d'une réalisation.
    Affiche toutes les informations du projet, y compris les trois images si elles existent.
    """
    categorie_display = serializers.CharField(source='get_categorie_display', read_only=True)
    
    class Meta:
        model = Realisation
        fields = '__all__'


class RealisationCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la création et la mise à jour d'une réalisation.
    Inclut la validation des champs requis.
    """
    class Meta:
        model = Realisation
        fields = '__all__'
        
    def validate_categorie(self, value):
        """Valide que la catégorie est l'une des valeurs autorisées."""
        # Vérifier si la valeur est présente dans les choix de catégorie
        if value not in dict(Categorie.choices):
            raise serializers.ValidationError(
                f"La catégorie '{value}' n'est pas valide. Les valeurs autorisées sont: "
                f"{', '.join([f'{key} ({val})' for key, val in Categorie.choices])}"
            )
        return value