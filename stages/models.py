from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

#class DomaineStage(models.Model):
 #   """
 #   Modèle représentant un domaine de stage disponible.
    
  #  Attributes:
   #     nom (str): Nom unique du domaine de stage
    #    description (str): Description détaillée du domaine
    #"""
    #nom = models.CharField(max_length=100, unique=True)
    #description = models.TextField(blank=True, null=True)
    
    #def __str__(self):
    #    return self.nom

def test_smtp_connection():
    try:
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.quit()
        return True
    except Exception as e:
        logger.error(f"Erreur de connexion SMTP: {str(e)}")
        return False

class OffreStage(models.Model):
    """
    Modèle représentant une offre de stage.
    
    Attributes:
        titre (str): Titre de l'offre de stage
        description (str): Description détaillée du stage
        date_debut (date): Date de début du stage
        duree (int): Durée du stage en semaines
        competences (str): Compétences requises pour le stage
        mission (str): Description de la mission
    """
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_debut = models.DateField()
    duree = models.IntegerField(help_text="Durée en semaines")
    competences = models.TextField()
    mission = models.TextField()
    
    def __str__(self):
        return self.titre

class DemandeStage(models.Model):
    """
    Modèle représentant une demande de stage.
    
    Attributes:
        utilisateur (User): Utilisateur associé à la demande (optionnel)
        email (str): Email du candidat
        cv (File): Fichier CV du candidat
        offre (OffreStage): Offre de stage choisie
        requete (str): Message/motivation du candidat
        statut (str): Statut de la demande (en_cours, accepte, refuse)
        date_demande (datetime): Date de création de la demande
        date_modification (datetime): Date de dernière modification
    """
    STATUT_CHOICES = [
        ('en_cours', 'En cours de traitement'),
        ('accepte', 'Accepté'),
        ('refuse', 'Refusé'),
    ]
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    cv = models.FileField(upload_to='cvs/')
    offre = models.ForeignKey(OffreStage, on_delete=models.CASCADE)
    #requete = models.TextField()
    lettre_motivation = models.FileField(upload_to='lettres_motivation/')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_cours')
    date_demande = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.email} - {self.offre.titre} - {self.statut}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_instance = None
        if not is_new:
            old_instance = DemandeStage.objects.get(pk=self.pk)
        
        super().save(*args, **kwargs)
        
        try:
            # Test de la connexion SMTP avant d'envoyer l'email
            if not test_smtp_connection():
                logger.error("Impossible de se connecter au serveur SMTP")
                raise Exception("Erreur de connexion SMTP")
            
            # Envoi d'email lors de la création d'une nouvelle demande
            if is_new:
                logger.info(f"Tentative d'envoi d'email de confirmation à {self.email}")
                logger.info(f"Configuration email: HOST={settings.EMAIL_HOST}, PORT={settings.EMAIL_PORT}, USER={settings.EMAIL_HOST_USER}")
                
                # Création d'un message à envoyer
                msg = MIMEMultipart()
                send_mail(
                    'Confirmation de votre demande de stage',
                    f'Votre demande de stage pour "{self.offre.titre}" a bien été reçue. Nous vous contacterons bientôt.',
                    settings.DEFAULT_FROM_EMAIL,
                    [self.email],
                    fail_silently=False,
                )
                logger.info(f"Email de confirmation envoyé avec succès à {self.email}")
            
            # Envoi d'email lors du changement de statut
            elif old_instance and old_instance.statut != self.statut:
                logger.info(f"Tentative d'envoi d'email de changement de statut à {self.email}")
                if self.statut == 'accepte':
                    message = f'Votre demande de stage pour "{self.offre.titre}" a été acceptée. Nous vous contacterons pour la suite.'
                else:
                    message = f'Votre demande de stage pour "{self.offre.titre}" a été refusée. Nous vous remercions de votre intérêt.'
                
                send_mail(
                    f'Statut de votre demande de stage - {self.statut}',
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [self.email],
                    fail_silently=False,
                )
                logger.info(f"Email de changement de statut envoyé avec succès à {self.email}")
        
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi de l'email: {str(e)}")
            # On lève l'exception pour voir l'erreur dans la console    pour le test
            raise