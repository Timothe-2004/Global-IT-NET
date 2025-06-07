from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Administrateur

@receiver(post_save, sender=User)
def ajouter_admin_automatiquement(sender, instance, created, **kwargs):
    if instance.is_superuser:
        admin_obj, created = Administrateur.objects.get_or_create(id=1)
        admin_obj.utilisateurs.add(instance)
