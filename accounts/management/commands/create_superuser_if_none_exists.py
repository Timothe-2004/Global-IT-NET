from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Créer un superuser automatiquement si il n\'existe pas'

    def handle(self, *args, **options):
        # Récupérer les identifiants depuis les variables d'environnement ou utiliser les valeurs par défaut
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        # Vérifier si un superuser existe déjà
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(
                self.style.WARNING('Un superuser existe déjà.')
            )
            return

        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'L\'utilisateur "{username}" existe déjà.')
            )
            return        # Créer le superuser
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" créé avec succès!')
            )
            
            # Créer également l'objet Administrateur associé
            from accounts.models import Administrateur
            admin, created = Administrateur.objects.get_or_create()
            admin.utilisateurs.add(user)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Objet Administrateur créé et associé à "{username}"'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Utilisateur "{username}" ajouté aux administrateurs existants'
                    )
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erreur lors de la création du superuser: {e}')
            )
