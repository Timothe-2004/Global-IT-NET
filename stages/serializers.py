from rest_framework import serializers
from .models import OffreStage, DemandeStage

class OffreStageSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle OffreStage.
    
    Permet la sérialisation et désérialisation des offres de stage.
    Inclut tous les champs du modèle.
    """
    class Meta:
        model = OffreStage
        fields = '__all__'

class DemandeStageSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle DemandeStage.
    
    Permet la sérialisation et désérialisation des demandes de stage.
    Les champs sensibles sont en lecture seule.
    """
    # Champ supplémentaire pour le titre de l'offre, en lecture seule
    offre_titre = serializers.CharField(source='offre.titre', read_only=True)
    
    class Meta:
        model = DemandeStage
        fields = ['id', 'nom', 'prenom', 'email', 'cv', 'offre', 'offre_titre', 
                 'lettre_motivation', 'statut', 'date_demande', 'date_modification']
        read_only_fields = ['statut', 'date_demande', 'date_modification']
        
    def validate_email(self, value):
        """
        Validation personnalisée pour l'email.
        """
        if not value:
            raise serializers.ValidationError("L'email est requis")
        return value
        
    def validate_cv(self, value):
        """
        Validation personnalisée pour le CV.
        """
        if not value:
            raise serializers.ValidationError("Le CV est requis")
        return value
        
    def validate_lettre_motivation(self, value):
        """
        Validation personnalisée pour la lettre de motivation.
        """
        if not value:
            raise serializers.ValidationError("La lettre de motivation est requise")
        return value

#class VerificationStatutSerializer(serializers.Serializer):
    #"""
    #Sérialiseur pour la vérification du statut d'une demande.
    #Utilisé uniquement pour la validation du code unique.
    #"""
    # Champ pour le code unique de la demande
    #code_unique = serializers.UUIDField()

class StatutDemandeSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour l'affichage du statut d'une demande.
    Version simplifiée du DemandeStageSerializer.
    """
    # Champ supplémentaire pour le nom du domaine, en lecture seule
    domaine_nom = serializers.CharField(source='domaine.nom', read_only=True)
    
    class Meta:
        # Définition du modèle associé
        model = DemandeStage
        # Liste des champs à inclure dans la sérialisation
        fields = ['code_unique', 'email', 'domaine_nom', 'statut', 'date_demande'] 