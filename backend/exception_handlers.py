from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Gestionnaire d'exception personnalisé pour DRF.
    Log les erreurs et retourne des réponses formatées.
    """
    # Appel du gestionnaire d'exception par défaut de DRF
    response = exception_handler(exc, context)

    if response is not None:
        # Log l'erreur pour le debug
        logger.error(f"API Error: {exc} - Context: {context}")
        
        # Personnaliser la réponse d'erreur
        custom_response_data = {
            'error': True,
            'message': 'Une erreur est survenue',
            'details': response.data if hasattr(response, 'data') else str(exc)
        }
        
        # Ajouter des informations de debug si en mode développement
        if hasattr(context, 'request') and context['request']:
            request = context['request']
            if hasattr(request, 'user') and request.user.is_authenticated and request.user.is_staff:
                custom_response_data['debug'] = {
                    'exception': str(exc),
                    'view': context.get('view', None).__class__.__name__ if context.get('view') else None,
                    'request_path': request.path if hasattr(request, 'path') else None
                }
        
        response.data = custom_response_data

    else:
        # Si DRF n'a pas géré l'exception, la gérer nous-mêmes
        logger.error(f"Unhandled API Error: {exc} - Context: {context}")
        
        response = Response({
            'error': True,
            'message': 'Erreur interne du serveur',
            'details': 'Une erreur inattendue s\'est produite'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
