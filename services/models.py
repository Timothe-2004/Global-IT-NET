from django.db import models
from django.utils.translation import gettext_lazy as _

class Service(models.Model):
    """
    Modèle représentant un service proposé par l'entreprise.
    """
    titre = models.CharField(_('Titre'), max_length=255, help_text=_('Titre du service'))
    sous_titre = models.CharField(_('Sous-titre'), max_length=255, help_text=_('Sous-titre descriptif du service'))
    image = models.ImageField(_('Image'), upload_to='services/', blank=True, null=True, help_text=_('Image illustrant le service'))
    description = models.TextField(_('Description'), help_text=_('Description détaillée du service'))    
    details = models.JSONField(_('Détails'), default=list, help_text=_('Liste de 3 détails avec spécificité et détail'))

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['titre']  # Tri par titre (alphabétique)

    def __str__(self):
        """Représentation textuelle d'un service."""
        return self.titre

    def clean(self):
        """Validation des données."""
        from django.core.exceptions import ValidationError
        
        # Validation du champ details
        if self.details:
            if not isinstance(self.details, list):
                raise ValidationError(_('Le champ détails doit être une liste.'))
            
            if len(self.details) > 3:
                raise ValidationError(_('Maximum 3 détails autorisés.'))
            
            for detail in self.details:
                if not isinstance(detail, dict):
                    raise ValidationError(_('Chaque détail doit être un objet avec "specificite" et "detail".'))
                
                if 'specificite' not in detail or 'detail' not in detail:
                    raise ValidationError(_('Chaque détail doit contenir "specificite" et "detail".'))
                
                if not detail.get('specificite') or not detail.get('detail'):
                    raise ValidationError(_('Les champs "specificite" et "detail" ne peuvent pas être vides.'))

    @property
    def image_principale(self):
        """Renvoie l'image principale ou None si aucune n'est définie."""
        return self.image if self.image else None
