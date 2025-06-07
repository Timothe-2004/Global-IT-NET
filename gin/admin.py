from django.contrib import admin
from .models import Formation
# Register your models here.

@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display=('titre','description','date_debut','date_fin','lieu')
    search_fields=['titre']

