from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Utilisateur, Inscription, RechercheFormation
from datetime import date, timedelta
import json
from unittest.mock import patch
from django.conf import settings

# Configuration pour les tests
settings.FORMATION_API_URL = 'http://test-api.example.com'
settings.FORMATION_API_KEY = 'test-key'

class UtilisateurTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.valid_payload = {
            'user': {
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpass123',
                'first_name': 'Test',
                'last_name': 'User'
            },
            'telephone': '0123456789',
            'adresse': '123 Test Street',
            'date_naissance': '1990-01-01'
        }

    def test_create_utilisateur(self):
        response = self.client.post(
            self.register_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Utilisateur.objects.count(), 1)
        self.assertEqual(Utilisateur.objects.get().user.username, 'testuser')

    def test_create_utilisateur_invalid_date(self):
        invalid_payload = self.valid_payload.copy()
        invalid_payload['date_naissance'] = (date.today() + timedelta(days=1)).isoformat()
        response = self.client.post(
            self.register_url,
            data=json.dumps(invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        # Créer un utilisateur
        self.client.post(
            self.register_url,
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        
        # Tester la connexion
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(
            self.login_url,
            data=json.dumps(login_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

class InscriptionTests(APITestCase):
    def setUp(self):
        # Créer un utilisateur
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.utilisateur = Utilisateur.objects.create(
            user=self.user,
            telephone='0123456789'
        )
        
        # URLs
        self.inscription_url = reverse('inscription')
        self.recherche_url = reverse('recherche-formation')
        
        # Authentifier l'utilisateur
        self.client.force_authenticate(user=self.user)

    def test_create_inscription(self):
        inscription_data = {
            'formation_id': '123',
            'formation_nom': 'Test Formation'
        }
        response = self.client.post(
            self.inscription_url,
            data=json.dumps(inscription_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Inscription.objects.count(), 1)
        self.assertEqual(Inscription.objects.get().formation_nom, 'Test Formation')

    @patch('requests.get')
    def test_recherche_formation(self, mock_get):
        # Configurer le mock
        mock_get.return_value.json.return_value = [
            {
                'id': '1',
                'nom': 'Python Formation',
                'description': 'Test Description',
                'date_debut': '2024-01-01',
                'date_fin': '2024-12-31'
            }
        ]
        mock_get.return_value.status_code = 200

        recherche_data = {
            'terme_recherche': 'python'
        }
        response = self.client.post(
            self.recherche_url,
            data=json.dumps(recherche_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RechercheFormation.objects.count(), 1)
        self.assertEqual(RechercheFormation.objects.get().terme_recherche, 'python')

class RechercheFormationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.utilisateur = Utilisateur.objects.create(
            user=self.user,
            telephone='0123456789'
        )
        self.recherche_url = reverse('recherche-formation')
        self.client.force_authenticate(user=self.user)

    def test_recherche_sans_terme(self):
        response = self.client.post(
            self.recherche_url,
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('requests.get')
    def test_recherche_avec_terme(self, mock_get):
        # Configurer le mock
        mock_get.return_value.json.return_value = [
            {
                'id': '1',
                'nom': 'Python Formation',
                'description': 'Test Description',
                'date_debut': '2024-01-01',
                'date_fin': '2024-12-31'
            }
        ]
        mock_get.return_value.status_code = 200

        response = self.client.post(
            self.recherche_url,
            data=json.dumps({'terme_recherche': 'python'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(RechercheFormation.objects.count(), 1)
