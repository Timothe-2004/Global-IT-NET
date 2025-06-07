from django.db import models
from django.utils.translation import gettext_lazy as _

class Categorie(models.TextChoices):
    """Catégories disponibles pour les réalisations."""
    DEV_WEB = 'DEV_WEB', _('Développement web')
    DEV_MOBILE = 'DEV_MOBILE', _('Développement mobile')
    CYBERSECURITE = 'CYBERSECURITE', _('Cybersécurité')
    RESEAU_INFRA = 'RESEAU_INFRA', _('Réseau et Infrastructure')
    IA = 'IA', _('Intelligence Artificielle')

class Realisation(models.Model):
    """
    Modèle représentant une réalisation (projet réalisé) avec toutes ses informations.
    """
    nomProjet = models.CharField(_('Nom du projet'), max_length=255, help_text=_('Entrez le nom du projet'))
    description = models.TextField(_('Description'), help_text=_('Description détaillée du projet'))
    categorie = models.CharField(
        _('Catégorie'), 
        max_length=20, 
        choices=Categorie.choices, 
        help_text=_('Sélectionnez la catégorie du projet')
    )
    client = models.CharField(_('Client'), max_length=255, blank=True, null=True, help_text=_('Nom du client (optionnel)'))
    dateDebut = models.DateField(_('Date de début'), help_text=_('Date de début du projet'))
    dateFin = models.DateField(_('Date de fin'), blank=True, null=True, help_text=_('Date de fin du projet (optionnel)'))
    mission = models.TextField(_('Mission'), help_text=_('Décrivez la mission du projet'))
    challenge = models.TextField(_('Challenge'), blank=True, null=True, help_text=_('Décrivez les défis rencontrés'))
    solution = models.TextField(_('Solution'), blank=True, null=True, help_text=_('Décrivez les solutions apportées'))
    resultat = models.TextField(_('Résultat'), blank=True, null=True, help_text=_('Décrivez les résultats obtenus'))
    image1 = models.ImageField(_('Image principale'), upload_to='realisations/', blank=True, null=True, help_text=_('Téléchargez l\'image principale'))
    image2 = models.ImageField(_('Image secondaire 1'), upload_to='realisations/', blank=True, null=True, help_text=_('Téléchargez une image secondaire'))
    image3 = models.ImageField(_('Image secondaire 2'), upload_to='realisations/', blank=True, null=True, help_text=_('Téléchargez une autre image secondaire'))

    class Meta:
        verbose_name = _('Réalisation')
        verbose_name_plural = _('Réalisations')
        ordering = ['-dateDebut']  # Tri par date de début (du plus récent au plus ancien)

    def __str__(self):
        """Représentation textuelle d'une réalisation."""
        return f"{self.nomProjet} ({self.get_categorie_display()})"

    @property
    def image_principale(self):
        """Renvoie la première image disponible, ou None si aucune n'est définie."""
        if self.image1:
            return self.image1
        return None