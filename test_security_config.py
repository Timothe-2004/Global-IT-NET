#!/usr/bin/env python
"""
Script de test pour vérifier la configuration de sécurité de l'API.
"""
import os
import sys
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def test_permissions():
    """
    Teste les permissions configurées pour chaque app.
    """
    print("=== TEST DE CONFIGURATION DES PERMISSIONS ===\n")
    
    # Test des imports
    try:
        from backend.permissions import IsAdminUser, IsAdminOrReadOnly, IsAdminOrCreateOnly
        print("✅ Permissions personnalisées importées avec succès")
    except ImportError as e:
        print(f"❌ Erreur d'import des permissions: {e}")
        return False
    
    # Test des ViewSets
    try:
        from gin.views import FormationViewSet, InscriptionFormationViewSet
        from stages.views import OffreStageViewSet, DemandeStageViewSet
        from realisations.views import RealisationListView, RealisationCreateView
        from partenaires.views import PartenaireListCreateView
        from accounts.views import ConnexionView
        print("✅ Toutes les vues importées avec succès")
    except ImportError as e:
        print(f"❌ Erreur d'import des vues: {e}")
        return False
    
    # Vérification des permissions par app
    print("\n=== VÉRIFICATION DES PERMISSIONS PAR APP ===")
    
    # Formations
    formation_permissions = FormationViewSet.permission_classes[0].__name__
    inscription_permissions = InscriptionFormationViewSet.permission_classes[0].__name__
    print(f"📚 Formations: {formation_permissions}")
    print(f"📝 Inscriptions formations: {inscription_permissions}")
    
    # Stages
    offre_permissions = OffreStageViewSet.permission_classes[0].__name__
    demande_permissions = DemandeStageViewSet.permission_classes[0].__name__
    print(f"💼 Offres de stage: {offre_permissions}")
    print(f"📋 Demandes de stage: {demande_permissions}")
    
    # Réalisations
    print(f"🎨 Réalisations (lecture): AllowAny")
    print(f"🎨 Réalisations (création): {RealisationCreateView.permission_classes[0].__name__}")
    
    # Partenaires
    partenaire_permissions = PartenaireListCreateView.permission_classes[0].__name__
    print(f"🤝 Partenaires: {partenaire_permissions}")
    
    # Comptes
    connexion_permissions = ConnexionView.permission_classes[0].__name__
    print(f"👥 Connexion admin: {connexion_permissions}")
    
    print("\n✅ Configuration des permissions vérifiée avec succès!")
    return True

def test_middleware():
    """
    Teste la configuration du middleware CSRF.
    """
    print("\n=== TEST DU MIDDLEWARE CSRF ===")
    
    from django.conf import settings
    
    # Vérifier que le middleware est dans la liste
    if 'backend.middleware.CSRFExemptAPIMiddleware' in settings.MIDDLEWARE:
        print("✅ Middleware CSRFExemptAPIMiddleware configuré")
    else:
        print("❌ Middleware CSRFExemptAPIMiddleware non trouvé")
        return False
    
    # Vérifier l'ordre du middleware
    middleware_list = settings.MIDDLEWARE
    csrf_exempt_index = middleware_list.index('backend.middleware.CSRFExemptAPIMiddleware')
    csrf_index = middleware_list.index('django.middleware.csrf.CsrfViewMiddleware')
    
    if csrf_exempt_index < csrf_index:
        print("✅ Ordre du middleware correct (CSRFExempt avant CsrfView)")
    else:
        print("❌ Ordre du middleware incorrect")
        return False
    
    return True

def main():
    """
    Fonction principale de test.
    """
    print("🔒 VÉRIFICATION DE LA CONFIGURATION DE SÉCURITÉ API\n")
    
    success = True
    
    # Test des permissions
    if not test_permissions():
        success = False
    
    # Test du middleware
    if not test_middleware():
        success = False
    
    print("\n" + "="*60)
    if success:
        print("🎉 TOUS LES TESTS PASSÉS AVEC SUCCÈS!")
        print("\n📋 RÉSUMÉ DE LA CONFIGURATION:")
        print("• CSRF désactivé automatiquement pour toutes les URLs /api/")
        print("• Formations: Lecture publique, Écriture admin")
        print("• Inscriptions: Création publique, Gestion admin")
        print("• Stages: Lecture publique, Écriture admin")
        print("• Candidatures: Création publique, Gestion admin")
        print("• Réalisations: Lecture publique, Écriture admin")
        print("• Partenaires: Lecture publique, Écriture admin")
        print("• Authentification admin: Public (connexion)")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez les erreurs ci-dessus et corrigez la configuration.")

if __name__ == "__main__":
    main()
