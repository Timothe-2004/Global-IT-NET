"""
Serializers pour le module accounts.
Ces serializers gèrent la sérialisation et la validation des données d'authentification.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Administrateur


class UtilisateurSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour l'affichage des informations de l'utilisateur.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        read_only_fields = ['id', 'is_staff']


class AdministrateurSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour l'affichage des informations de l'administrateur.
    """
    utilisateur = UtilisateurSerializer(read_only=True)
    
    class Meta:
        model = Administrateur
        fields = ['id', 'utilisateur', 'date_creation']
        read_only_fields = ['id', 'date_creation']


class ConnexionSerializer(serializers.Serializer):
    """
    Sérialiseur pour la connexion de l'administrateur.
    """
    username = serializers.CharField(
        label="Nom d'utilisateur",
        write_only=True
    )
    
    password = serializers.CharField(
        label="Mot de passe",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    
    def validate(self, attrs):
        """
        Valide les informations de connexion et authentifie l'utilisateur.
        """
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Tentative d'authentification
            user = authenticate(request=self.context.get('request'),
                              username=username, password=password)
            if not user:
                msg = 'Impossible de se connecter avec les identifiants fournis.'
                raise serializers.ValidationError(msg, code='authorization')
            
            # Vérifier que l'utilisateur est bien un administrateur
            admin = Administrateur.objects.filter(utilisateurs=user).first()
            if not admin:
                raise serializers.ValidationError("Vous n'êtes pas un administrateur.")
                
        else:
            msg = 'Le nom d\'utilisateur et le mot de passe sont requis.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
