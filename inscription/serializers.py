# inscription/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Utilisateur, Inscription, RechercheFormation
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UtilisateurSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    date_naissance = serializers.DateField(required=False)

    class Meta:
        model = Utilisateur
        fields = ('id', 'user', 'telephone', 'adresse', 'date_naissance')

    def validate_date_naissance(self, value):
        if value and value > date.today():
            raise serializers.ValidationError("La date de naissance ne peut pas être dans le futur")
        return value

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        utilisateur = Utilisateur.objects.create(user=user, **validated_data)
        return utilisateur

class InscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscription
        fields = ('id', 'utilisateur', 'formation_id', 'formation_nom', 'date_inscription')
        read_only_fields = ('date_inscription',)

class RechercheFormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RechercheFormation
        fields = ('id', 'utilisateur', 'terme_recherche', 'date_recherche')
        read_only_fields = ('date_recherche',)

class FormationExterneSerializer(serializers.Serializer):
    id = serializers.CharField()
    nom = serializers.CharField()
    description = serializers.CharField(required=False)
    date_debut = serializers.DateField()
    date_fin = serializers.DateField()
    prix = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    lieu = serializers.CharField(required=False)
    capacite = serializers.IntegerField(required=False)

    def validate(self, data):
        if data.get('date_debut') and data.get('date_fin'):
            if data['date_debut'] > data['date_fin']:
                raise serializers.ValidationError("La date de début doit être antérieure à la date de fin")
        return data
