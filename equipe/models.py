from django.db import models
from django.utils.translation import gettext_lazy as _

class Employe(models.Model):
    """
    Modèle représentant un employé de l'équipe de l'entreprise.
    """
    nom = models.CharField(_('Nom'), max_length=100, help_text=_('Nom de famille de l\'employé'))
    prenom = models.CharField(_('Prénom'), max_length=100, help_text=_('Prénom de l\'employé'))
    photo = models.ImageField(_('Photo'), upload_to='equipe/', blank=True, null=True, help_text=_('Photo de profil de l\'employé'))
    poste = models.CharField(_('Poste'), max_length=255, help_text=_('Intitulé du poste de l\'employé'))
    actif = models.BooleanField(_('Actif'), default=True, help_text=_('Indique si l\'employé est toujours dans l\'équipe'))

    class Meta:
        verbose_name = _('Employé')
        verbose_name_plural = _('Employés')
        ordering = ['nom', 'prenom']  # Tri par nom puis prénom

    def __str__(self):
        """Représentation textuelle d'un employé."""
        return f"{self.prenom} {self.nom} - {self.poste}"

    @property
    def nom_complet(self):
        """Retourne le nom complet de l'employé."""
        return f"{self.prenom} {self.nom}"

    @property
    def photo_principale(self):
        """Renvoie la photo principale ou None si aucune n'est définie."""
        return self.photo if self.photo else None
