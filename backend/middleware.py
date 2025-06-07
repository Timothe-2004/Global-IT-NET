"""
Middleware personnalisé pour gérer la sécurité des APIs.
"""
import re
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class CSRFExemptAPIMiddleware(MiddlewareMixin):
    """
    Middleware qui désactive la vérification CSRF pour toutes les URLs d'API.
    Toutes les URLs commençant par /api/ sont exemptées de CSRF.
    """
    
    def process_request(self, request):
        """
        Marque la requête comme exemptée de CSRF si c'est une API.
        """
        # Vérifier si l'URL correspond à une API
        if request.path_info.startswith('/api/'):
            # Marquer cette requête comme exemptée de CSRF
            setattr(request, '_dont_enforce_csrf_checks', True)
        
        return None
