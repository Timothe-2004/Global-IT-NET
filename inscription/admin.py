from django.contrib import admin
from .models import Utilisateur, Inscription, RechercheFormation
# Register your models here.

admin.site.register(Inscription)
admin.site.register(Utilisateur)
admin.site.register(RechercheFormation)
