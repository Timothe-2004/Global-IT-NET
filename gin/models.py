from django.db import models
from django.core.exceptions import ValidationError

class Formation(models.Model):
    titre = models.CharField(max_length=100)
    description = models.TextField()
    objectifs = models.JSONField(default=list)
    
    # Programme structuré : liste de modules (section + contenus)
    programme = models.JSONField(default=list)

    prerecquis = models.JSONField(default=list)
    acquis = models.TextField(verbose_name="acquis")
    debouche = models.TextField(verbose_name="Débouchés")
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    lieu = models.CharField(max_length=100)

    def __str__(self):
        return self.titre

    def clean(self):
        if self.date_fin and self.date_fin < self.date_debut:
            raise ValidationError("La date de fin doit être postérieure à la date de début.")
        

class InscriptionFormation(models.Model):
    DIPLOME_CHOICES = [
        ('BEPC', 'BEPC'),
        ('BAC', 'Bac'),
        ('LICENCE', 'Licence'),
        ('MASTER', 'Master'),
        ('DOCTORAT', 'Doctorat'),
    ]

    formation = models.ForeignKey('Formation', on_delete=models.CASCADE, related_name='inscriptions')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    motivations = models.TextField()
    dernier_diplome = models.CharField(max_length=10, choices=DIPLOME_CHOICES)
    domaine = models.CharField(max_length=100)
    annees_experience = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.formation.titre}"

