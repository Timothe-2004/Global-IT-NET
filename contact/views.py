from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, OpenApiExample
import logging
from .serializers import ContactSerializer
from .models import Contact

logger = logging.getLogger(__name__)

class ContactView(APIView):
    """
    Vue pour gérer les messages de contact.
    Accessible à tous (pas d'authentification requise).
    """
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Envoyer un message de contact",
        description="Permet d'envoyer un message de contact qui sera envoyé par email aux administrateurs.",
        request=ContactSerializer,
        responses={
            201: ContactSerializer,
            400: 'Données invalides',
            500: 'Erreur lors de l\'envoi de l\'email'
        },
        examples=[
            OpenApiExample(
                name="Exemple de message de contact",
                value={
                    "name": "Jean Dupont",
                    "email": "jean.dupont@example.com",
                    "subject": "Demande d'information",
                    "message": "Bonjour, je souhaiterais obtenir plus d'informations sur vos services de développement web."
                },
                request_only=True
            )
        ]
    )
    def post(self, request, format=None):
        """Envoie un message de contact."""
        serializer = ContactSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                # Sauvegarder le message en base
                contact = serializer.save()
                logger.info(f"Nouveau message de contact reçu de {contact.email}")
                
                # Préparer l'email
                subject = f"🔔 Nouveau message de contact: {contact.subject}"
                message = f"""
Nouveau message de contact reçu sur le site web GIN :

👤 Nom: {contact.name}
📧 Email: {contact.email}
📝 Sujet: {contact.subject}

💬 Message:
{contact.message}

🕒 Reçu le: {contact.created_at.strftime('%d/%m/%Y à %H:%M')}

---
Ce message a été envoyé automatiquement depuis le formulaire de contact du site web.
                """
                
                # Envoyer l'email
                try:
                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.CONTACT_EMAIL],
                        fail_silently=False,
                    )
                    logger.info(f"Email de contact envoyé avec succès pour {contact.email}")
                    
                    return Response({
                        'message': 'Votre message a été envoyé avec succès. Nous vous répondrons dans les plus brefs délais.',
                        'contact': serializer.data
                    }, status=status.HTTP_201_CREATED)
                    
                except Exception as e:
                    logger.error(f"Erreur lors de l'envoi de l'email de contact: {str(e)}")
                    # Le message est sauvegardé même si l'email échoue
                    return Response({
                        'message': 'Votre message a été enregistré mais une erreur est survenue lors de l\'envoi de l\'email. Nos équipes ont été notifiées.',
                        'contact': serializer.data
                    }, status=status.HTTP_201_CREATED)
                    
            except Exception as e:
                logger.error(f"Erreur lors de la sauvegarde du message de contact: {str(e)}")
                return Response({
                    'error': 'Une erreur est survenue lors de l\'enregistrement de votre message. Veuillez réessayer.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        return Response({
            'error': 'Données invalides',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
