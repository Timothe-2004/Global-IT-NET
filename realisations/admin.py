from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Realisation

@admin.register(Realisation)
class RealisationAdmin(admin.ModelAdmin):
    """Administration des réalisations."""
    list_display = ('nomProjet', 'categorie', 'client', 'dateDebut', 'dateFin')
    list_filter = ('categorie', 'dateDebut')
    search_fields = ('nomProjet', 'description', 'client', 'mission')
    date_hierarchy = 'dateDebut'
    fieldsets = (
        (_('Informations générales'), {
            'fields': ('nomProjet', 'description', 'categorie', 'client')
        }),
        (_('Dates'), {
            'fields': ('dateDebut', 'dateFin')
        }),
        (_('Détails du projet'), {
            'fields': ('mission', 'challenge', 'solution', 'resultat')
        }),
        (_('Images'), {
            'fields': ('image1', 'image2', 'image3')
        }),
    )