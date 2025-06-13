from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Employe

@admin.register(Employe)
class EmployeAdmin(admin.ModelAdmin):
    """Administration des employés de l'équipe."""
    list_display = ('nom_complet', 'poste', 'actif')
    list_filter = ('actif', 'poste')
    search_fields = ('nom', 'prenom', 'poste')
    list_editable = ('actif',)
    
    fieldsets = (
        (_('Informations personnelles'), {
            'fields': ('nom', 'prenom', 'photo', 'poste')
        }),
        (_('Statut'), {
            'fields': ('actif',)
        }),
    )

    def nom_complet(self, obj):
        """Affiche le nom complet dans la liste."""
        return obj.nom_complet
    nom_complet.short_description = _('Nom complet')
    nom_complet.admin_order_field = 'nom'

    def get_queryset(self, request):
        """Optimisation des requêtes."""
        queryset = super().get_queryset(request)
        return queryset.select_related()

    actions = ['marquer_actif', 'marquer_inactif']

    def marquer_actif(self, request, queryset):
        """Action pour marquer les employés comme actifs."""
        queryset.update(actif=True)
        self.message_user(request, _('Employés marqués comme actifs.'))
    marquer_actif.short_description = _('Marquer comme actif')

    def marquer_inactif(self, request, queryset):
        """Action pour marquer les employés comme inactifs."""
        queryset.update(actif=False)
        self.message_user(request, _('Employés marqués comme inactifs.'))
    marquer_inactif.short_description = _('Marquer comme inactif')
