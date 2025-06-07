from django.contrib import admin
from .models import OffreStage, DemandeStage

@admin.register(OffreStage)
class OffreStageAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_debut', 'duree')
    search_fields = ('titre', 'description', 'competences')
    list_filter = ('date_debut', 'duree')
    ordering = ('-date_debut',)

@admin.register(DemandeStage)
class DemandeStageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'offre', 'statut', 'date_demande', 'date_modification')
    list_filter = ('statut', 'date_demande', 'offre')
    search_fields = ('nom', 'prenom', 'email')
    readonly_fields = ('date_demande', 'date_modification')
    actions = ['marquer_comme_accepte', 'marquer_comme_refuse']
    
    def marquer_comme_accepte(self, request, queryset):
        queryset.update(statut='accepte')
    marquer_comme_accepte.short_description = "Marquer les demandes sélectionnées comme acceptées"
    
    def marquer_comme_refuse(self, request, queryset):
        queryset.update(statut='refuse')
    marquer_comme_refuse.short_description = "Marquer les demandes sélectionnées comme refusées"