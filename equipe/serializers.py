from rest_framework import serializers
from .models import Employe

class EmployeSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Employe."""
    nom_complet = serializers.SerializerMethodField()
    photo_principale = serializers.SerializerMethodField()

    class Meta:
        model = Employe
        fields = '__all__'

    def get_nom_complet(self, obj):
        """Retourne le nom complet de l'employé."""
        return obj.nom_complet

    def get_photo_principale(self, obj):
        """Retourne l'URL de la photo principale."""
        if obj.photo_principale:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo_principale.url)
        return None

class EmployeListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des employés (vue simplifiée)."""
    nom_complet = serializers.SerializerMethodField()
    photo_principale = serializers.SerializerMethodField()

    class Meta:
        model = Employe
        fields = ('id', 'nom_complet', 'poste', 'photo_principale', 'actif')

    def get_nom_complet(self, obj):
        """Retourne le nom complet de l'employé."""
        return obj.nom_complet

    def get_photo_principale(self, obj):
        """Retourne l'URL de la photo principale."""
        if obj.photo_principale:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo_principale.url)
        return None

class EmployeCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la création et mise à jour des employés."""
    
    class Meta:
        model = Employe
        fields = ('nom', 'prenom', 'photo', 'poste', 'actif')
