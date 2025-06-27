from rest_framework import serializers
from .models import Contact
import re

class ContactSerializer(serializers.ModelSerializer):
    """Serializer pour les messages de contact."""
    
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['created_at']

    def validate_name(self, value):
        """Validation du nom."""
        if not value or not value.strip():
            raise serializers.ValidationError("Le nom ne peut pas être vide.")
        
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Le nom doit contenir au moins 2 caractères.")
            
        if len(value.strip()) > 100:
            raise serializers.ValidationError("Le nom ne peut pas dépasser 100 caractères.")
            
        return value.strip()

    def validate_email(self, value):
        """Validation de l'email."""
        if not value or not value.strip():
            raise serializers.ValidationError("L'email ne peut pas être vide.")
            
        # Validation basique de l'email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Format d'email invalide.")
            
        return value.lower().strip()

    def validate_subject(self, value):
        """Validation du sujet."""
        if not value or not value.strip():
            raise serializers.ValidationError("Le sujet ne peut pas être vide.")
            
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Le sujet doit contenir au moins 5 caractères.")
            
        if len(value.strip()) > 200:
            raise serializers.ValidationError("Le sujet ne peut pas dépasser 200 caractères.")
            
        return value.strip()

    def validate_message(self, value):
        """Validation du message."""
        if not value or not value.strip():
            raise serializers.ValidationError("Le message ne peut pas être vide.")
            
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Le message doit contenir au moins 10 caractères.")
            
        if len(value.strip()) > 5000:
            raise serializers.ValidationError("Le message ne peut pas dépasser 5000 caractères.")
            
        return value.strip()
