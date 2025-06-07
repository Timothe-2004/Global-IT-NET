"""
Définition des permissions personnalisées pour le projet.
"""

'''
from rest_framework import permissions
fro  m accounts.models import Administrateur

class EstAdministrateur(permissions.BasePermission):
    """
    Permission qui n'autorise que l'administrateur du site.
    """
    message = "Vous devez être administrateur pour effectuer cette action."
    
    def has_permission(self, request, view):
        """
        Vérifie si l'utilisateur est connecté et est un administrateur.
        """
        if not request.user.is_authenticated:
            return False
            
        try:
            from accounts.models import Administrateur
            return Administrateur.objects.filter(utilisateur=request.user).exists()
        except Exception:
            return False
        
'''