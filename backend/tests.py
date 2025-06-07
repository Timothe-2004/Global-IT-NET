"""
Tests pour les permissions personnalisées du projet.
"""
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User, AnonymousUser
from django.test import RequestFactory
from rest_framework.views import APIView
from accounts.models import Administrateur
from backend.permissions import EstAdministrateur

class TestView(APIView):
    """Vue de test pour vérifier les permissions."""
    permission_classes = [EstAdministrateur]
    
    def get(self, request):
        return None

class PermissionsTestCase(APITestCase):
    """Tests pour les classes de permissions personnalisées."""
    
    def setUp(self):
        """Configuration initiale pour les tests."""
        self.factory = RequestFactory()
        
        # Créer un utilisateur admin
        self.admin_user = User.objects.create_user(username="admin", password="adminpass")
        self.admin = Administrateur.objects.create()
        self.admin.utilisateurs.add(self.admin_user)
        
        # Créer un utilisateur normal
        self.normal_user = User.objects.create_user(username="user", password="userpass")
        
        # Instance de la vue de test
        self.view = TestView()
        
    def test_est_administrateur_permission_with_admin(self):
        """Test de la permission EstAdministrateur avec un utilisateur admin."""
        request = self.factory.get('/dummy/')
        request.user = self.admin_user
        permission = EstAdministrateur()
        self.assertTrue(permission.has_permission(request, self.view))
        
    def test_est_administrateur_permission_with_normal_user(self):
        """Test de la permission EstAdministrateur avec un utilisateur normal."""
        request = self.factory.get('/dummy/')
        request.user = self.normal_user
        permission = EstAdministrateur()
        self.assertFalse(permission.has_permission(request, self.view))
          def test_est_administrateur_permission_without_authentication(self):
        """Test de la permission EstAdministrateur sans authentification."""
        request = self.factory.get('/dummy/')
        request.user = AnonymousUser()
        permission = EstAdministrateur()
        self.assertFalse(permission.has_permission(request, self.view))
        
    def test_est_administrateur_message(self):
        """Test du message d'erreur de la permission EstAdministrateur."""
        permission = EstAdministrateur()
        self.assertEqual(permission.message, "Vous devez être administrateur pour effectuer cette action.")
