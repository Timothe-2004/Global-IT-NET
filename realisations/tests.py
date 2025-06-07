from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from accounts.models import Administrateur
from datetime import date
import tempfile
import os
from PIL import Image

from .models import Realisation, Categorie

class RealisationModelTestCase(TestCase):
    """Tests pour le modèle Realisation."""
    
    def setUp(self):
        """Configuration initiale pour les tests."""
        # Créer un fichier image temporaire pour les tests
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as img_file:
            image = Image.new('RGB', (100, 100), color='red')
            image.save(img_file, format='JPEG')
            self.image_path = img_file.name
            
        with open(self.image_path, 'rb') as img:
            self.image = SimpleUploadedFile(
                name='test_image.jpg',
                content=img.read(),
                content_type='image/jpeg'
            )
        
        self.realisation = Realisation.objects.create(
            nomProjet="Projet Test",
            description="Description du projet test",
            categorie=Categorie.DEV_WEB,
            dateDebut=date(2023, 1, 1),
            mission="Mission test",
            image1=self.image
        )
    
    def tearDown(self):
        """Nettoyage après les tests."""
        if os.path.exists(self.image_path):
            os.unlink(self.image_path)
    
    def test_str_representation(self):
        """Test de la représentation textuelle du modèle."""
        self.assertEqual(str(self.realisation), "Projet Test (Développement web)")
    
    def test_image_principale_property(self):
        """Test de la propriété image_principale."""
        self.assertEqual(self.realisation.image_principale, self.realisation.image1)
        
        # Tester avec une réalisation sans image
        realisation_sans_image = Realisation.objects.create(
            nomProjet="Projet Sans Image",
            description="Description du projet sans image",
            categorie=Categorie.IA,
            dateDebut=date(2023, 2, 1),
            mission="Mission test sans image"
        )
        self.assertIsNone(realisation_sans_image.image_principale)

class RealisationsAPITestCase(APITestCase):
    """Tests pour les API du module réalisations."""

    def setUp(self):
        """Configuration initiale pour les tests."""
        # Créer un utilisateur admin pour tester les fonctionnalités protégées
        self.admin_user = User.objects.create_user(username="admin", password="adminpass")
        self.admin = Administrateur.objects.create()
        self.admin.utilisateurs.add(self.admin_user)
        
        # Créer un utilisateur normal
        self.user = User.objects.create_user(username="user", password="userpass")
        
        # Créer des réalisations pour les tests
        self.realisation_web = Realisation.objects.create(
            nomProjet="Projet Web",
            description="Description du projet web",
            categorie=Categorie.DEV_WEB,
            dateDebut=date(2023, 1, 1),
            mission="Mission web"
        )
        
        self.realisation_mobile = Realisation.objects.create(
            nomProjet="Projet Mobile",
            description="Description du projet mobile",
            categorie=Categorie.DEV_MOBILE,
            dateDebut=date(2023, 2, 1),
            mission="Mission mobile"
        )
        
        # URLs pour les tests
        self.list_url = reverse('realisations:list')
        self.detail_url = reverse('realisations:detail', args=[self.realisation_web.id])
        self.create_url = reverse('realisations:realisation-create')
        self.update_url = reverse('realisations:realisation-update', args=[self.realisation_web.id])
        self.delete_url = reverse('realisations:realisation-delete', args=[self.realisation_web.id])
        self.categories_url = reverse('realisations:categorie-list')

    def test_list_realisations(self):
        """Test de la liste des réalisations."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_filter_realisations_by_category(self):
        """Test du filtrage des réalisations par catégorie."""
        response = self.client.get(f"{self.list_url}?categorie={Categorie.DEV_WEB}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nomProjet'], "Projet Web")
        
    def test_detail_realisation(self):
        """Test des détails d'une réalisation."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nomProjet"], "Projet Web")
        self.assertEqual(response.data["categorie"], Categorie.DEV_WEB)
        
    def test_create_realisation_unauthorized(self):
        """Test de la création d'une réalisation sans authentification."""
        data = {
            "nomProjet": "Nouveau Projet",
            "description": "Description du nouveau projet",
            "categorie": Categorie.IA,
            "dateDebut": "2023-03-01",
            "mission": "Nouvelle mission"
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_create_realisation_as_admin(self):
        """Test de la création d'une réalisation en tant qu'admin."""
        self.client.login(username="admin", password="adminpass")
        data = {
            "nomProjet": "Nouveau Projet",
            "description": "Description du nouveau projet",
            "categorie": Categorie.IA,
            "dateDebut": "2023-03-01",
            "mission": "Nouvelle mission"
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Realisation.objects.count(), 3)
        
    def test_update_realisation_as_admin(self):
        """Test de la mise à jour d'une réalisation en tant qu'admin."""
        self.client.login(username="admin", password="adminpass")
        data = {
            "nomProjet": "Projet Web Modifié",
            "description": "Description modifiée",
            "categorie": Categorie.DEV_WEB,
            "dateDebut": "2023-01-01",
            "mission": "Mission modifiée"
        }
        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.realisation_web.refresh_from_db()
        self.assertEqual(self.realisation_web.nomProjet, "Projet Web Modifié")
        
    def test_delete_realisation_as_admin(self):
        """Test de la suppression d'une réalisation en tant qu'admin."""
        self.client.login(username="admin", password="adminpass")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Realisation.objects.count(), 1)
        
    def test_categories_list(self):
        """Test de la liste des catégories."""
        response = self.client.get(self.categories_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('categories', response.data)
        
        # Vérifier que toutes les catégories du modèle sont présentes
        categories_from_response = {cat['id'] for cat in response.data['categories']}
        categories_from_model = set(dict(Categorie.choices).keys())
        self.assertTrue(categories_from_model.issubset(categories_from_response))
