from django.db import models
from django.conf import settings

class Utilisateur(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    telephone = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)
    date_naissance = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username


class Inscription(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    formation_id = models.CharField(max_length=100)  # ID de la formation dans le système externe
    formation_nom = models.CharField(max_length=255)  # Nom de la formation pour référence
    date_inscription = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.utilisateur.user.username} - {self.formation_nom}"


class RechercheFormation(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    terme_recherche = models.CharField(max_length=255)
    date_recherche = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Recherche de {self.utilisateur.user.username}: {self.terme_recherche}"
