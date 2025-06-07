"""
Module de gestion de l'administrateur.
Ce module définit les modèles et la logique d'authentification pour l'administrateur.
"""
from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _

class Administrateur(models.Model):
    """
    Modèle représentant les administrateurs du système.
    Les administrateurs sont liés à un groupe Django existant nommé 'Admin'.
    """
    utilisateurs = models.ManyToManyField(
        User,
        related_name='administrateurs',
        verbose_name=_("Comptes utilisateurs associés"),
        help_text=_("Comptes utilisateurs Django associés à ces administrateurs")
    )

    class Meta:
        verbose_name = _("Administrateur")
        verbose_name_plural = _("Administrateurs")

    def __str__(self):
        """Représentation textuelle des administrateurs."""
        return f"Administrateurs: {', '.join([user.username for user in self.utilisateurs.all()])}"
