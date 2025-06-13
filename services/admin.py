from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Administration des services de l'entreprise."""
    list_display = ('titre', 'sous_titre')
    search_fields = ('titre', 'sous_titre', 'description')
    
    fieldsets = (
        (_('Informations générales'), {
            'fields': ('titre', 'sous_titre', 'image', 'description')
        }),
        (_('Détails du service'), {
            'fields': ('details',),
            'description': _('Format JSON: [{"specificite": "...", "detail": "..."}, ...]')
        }),
    )

    def get_queryset(self, request):
        """Optimisation des requêtes."""
        queryset = super().get_queryset(request)
        return queryset.select_related()

    class Media:
        css = {
            'all': ('admin/css/widgets.css',)
        }
