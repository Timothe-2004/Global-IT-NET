"""
Définition des permissions personnalisées pour le projet.
"""
from rest_framework import permissions
from accounts.models import Administrateur


class IsAdminUser(permissions.BasePermission):
    """
    Permission qui n'autorise que les administrateurs du système.
    """
    message = "Vous devez être administrateur pour effectuer cette action."
    
    def has_permission(self, request, view):
        """
        Vérifie si l'utilisateur est connecté et est un administrateur.
        """
        if not request.user.is_authenticated:
            return False
            
        # Vérifier si l'utilisateur est un administrateur
        try:
            return Administrateur.objects.filter(utilisateurs=request.user).exists()
        except Exception:
            return False


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission qui permet la lecture à tous, mais l'écriture aux admins uniquement.
    """
    
    def has_permission(self, request, view):
        # Permissions de lecture pour tous
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permissions d'écriture pour les admins uniquement
        if not request.user.is_authenticated:
            return False
            
        try:
            return Administrateur.objects.filter(utilisateurs=request.user).exists()
        except Exception:
            return False


class IsAdminOrCreateOnly(permissions.BasePermission):
    """
    Permission qui permet la création à tous (inscriptions/candidatures)
    et toutes les autres actions aux admins uniquement.
    """
    
    def has_permission(self, request, view):
        # Permet les créations (POST) à tous
        if request.method == 'POST':
            return True
        
        # Toutes les autres actions nécessitent d'être admin
        if not request.user.is_authenticated:
            return False
            
        try:
            return Administrateur.objects.filter(utilisateurs=request.user).exists()
        except Exception:
            return False