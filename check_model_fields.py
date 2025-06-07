#!/usr/bin/env python
"""
Script pour vérifier les champs du modèle Administrateur et tester le serializer.
"""
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from accounts.models import Administrateur
from accounts.serializers import AdministrateurSerializer
from django.contrib.auth.models import User

def check_model_fields():
    """Vérifie les champs disponibles dans le modèle Administrateur."""
    print("=== VÉRIFICATION DES CHAMPS DU MODÈLE ADMINISTRATEUR ===")
    print("\nChamps disponibles dans le modèle Administrateur :")
    
    # Lister tous les champs
    for field in Administrateur._meta.get_fields():
        field_type = type(field).__name__
        print(f"  - {field.name} ({field_type})")
    
    # Informations détaillées sur le champ utilisateurs
    utilisateurs_field = Administrateur._meta.get_field('utilisateurs')
    print(f"\nDétails du champ 'utilisateurs' :")
    print(f"  - Type: {type(utilisateurs_field).__name__}")
    print(f"  - Modèle lié: {utilisateurs_field.related_model.__name__}")
    print(f"  - Related name: {utilisateurs_field.related_query_name()}")

def test_serializer():
    """Teste le serializer AdministrateurSerializer."""
    print("\n=== TEST DU SERIALIZER ADMINISTRATEUR ===")
    
    # Créer un utilisateur de test
    user, created = User.objects.get_or_create(
        username='test_admin',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'Admin'
        }
    )
    
    # Créer un administrateur de test
    admin, created = Administrateur.objects.get_or_create()
    admin.utilisateurs.add(user)
    
    # Tester le serializer
    serializer = AdministrateurSerializer(admin)
    print(f"Données sérialisées: {serializer.data}")
    
    # Vérifier que les champs sont corrects
    expected_fields = ['id', 'utilisateurs']
    actual_fields = list(serializer.data.keys())
    
    print(f"\nChamps attendus: {expected_fields}")
    print(f"Champs actuels: {actual_fields}")
    
    if set(expected_fields) == set(actual_fields):
        print("✅ Le serializer fonctionne correctement !")
    else:
        print("❌ Problème avec le serializer")

def check_database_consistency():
    """Vérifie la cohérence avec la base de données."""
    print("\n=== VÉRIFICATION DE LA BASE DE DONNÉES ===")
    
    try:
        # Tester une requête simple
        count = Administrateur.objects.count()
        print(f"Nombre d'administrateurs en base: {count}")
        
        # Tester les relations
        if count > 0:
            admin = Administrateur.objects.first()
            users_count = admin.utilisateurs.count()
            print(f"Nombre d'utilisateurs associés au premier admin: {users_count}")
            
        print("✅ Base de données cohérente !")
        
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")

if __name__ == "__main__":
    check_model_fields()
    test_serializer()
    check_database_consistency()
    print("\n=== RÉSUMÉ ===")
    print("Votre modèle Administrateur a les champs suivants :")
    print("  - id (AutoField)")
    print("  - utilisateurs (ManyToManyField vers User)")
    print("\nVotre serializer doit utiliser ces champs exactement.")
    print("Le champ 'date_creation' n'existe pas dans votre modèle actuel.")
