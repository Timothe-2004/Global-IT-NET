from rest_framework import serializers
from .models import Service

class DetailSerializer(serializers.Serializer):
    """Serializer pour les détails d'un service."""
    specificite = serializers.CharField(max_length=255)
    detail = serializers.CharField()

class ServiceSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Service."""
    details = DetailSerializer(many=True, required=False)
    image_principale = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = '__all__'

    def get_image_principale(self, obj):
        """Retourne l'URL de l'image principale."""
        if obj.image_principale:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_principale.url)
        return None

    def validate_details(self, value):
        """Validation des détails."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Les détails doivent être une liste.")
        
        if len(value) > 3:
            raise serializers.ValidationError("Maximum 3 détails autorisés.")
        
        for detail in value:
            if not isinstance(detail, dict):
                raise serializers.ValidationError("Chaque détail doit être un objet.")
            
            if 'specificite' not in detail or 'detail' not in detail:
                raise serializers.ValidationError("Chaque détail doit contenir 'specificite' et 'detail'.")
            
            if not detail.get('specificite') or not detail.get('detail'):
                raise serializers.ValidationError("Les champs 'specificite' et 'detail' ne peuvent pas être vides.")
        
        return value

class ServiceListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des services (vue simplifiée)."""
    image_principale = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ('id', 'titre', 'sous_titre', 'image_principale')

    def get_image_principale(self, obj):
        """Retourne l'URL de l'image principale."""
        if obj.image_principale:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image_principale.url)
        return None

class ServiceCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour la création et mise à jour des services."""
    details = DetailSerializer(many=True, required=False)

    class Meta:
        model = Service
        fields = ('titre', 'sous_titre', 'image', 'description', 'details')

    def validate_details(self, value):
        """Validation des détails."""
        if not isinstance(value, list):
            raise serializers.ValidationError("Les détails doivent être une liste.")
        
        if len(value) > 3:
            raise serializers.ValidationError("Maximum 3 détails autorisés.")
        
        for detail in value:
            if not isinstance(detail, dict):
                raise serializers.ValidationError("Chaque détail doit être un objet.")
            
            if 'specificite' not in detail or 'detail' not in detail:
                raise serializers.ValidationError("Chaque détail doit contenir 'specificite' et 'detail'.")
            
            if not detail.get('specificite') or not detail.get('detail'):
                raise serializers.ValidationError("Les champs 'specificite' et 'detail' ne peuvent pas être vides.")
        
        return value
