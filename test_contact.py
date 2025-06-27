#!/usr/bin/env python
"""
Script simple pour tester le module contact
Usage: python test_contact.py
"""
import requests
import json

def test_contact_api():
    """Teste l'API de contact"""
    print("🧪 Test du module contact...")
    print("-" * 50)
    
    # URL de l'API contact
    url = "http://localhost:8000/api/contact/"
    
    # Données de test
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test du formulaire de contact",
        "message": "Ceci est un message de test envoyé depuis le script Python. Si vous recevez cet email, la configuration fonctionne parfaitement !"
    }
    
    try:
        print(f"📤 Envoi de la requête vers: {url}")
        print(f"📋 Données: {json.dumps(data, indent=2, ensure_ascii=False)}")
        print("-" * 50)
        
        # Envoi de la requête POST
        response = requests.post(
            url, 
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📈 Code de réponse: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ SUCCESS! Message envoyé avec succès!")
            print("📧 Vérifiez votre boîte email: secretariat@globalitnet.bj")
            print(f"📄 Réponse du serveur: {response.json()}")
        else:
            print(f"❌ ERREUR! Code: {response.status_code}")
            print(f"📄 Réponse: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERREUR: Impossible de se connecter au serveur")
        print("💡 Assurez-vous que le serveur Django est lancé: python manage.py runserver")
        
    except requests.exceptions.Timeout:
        print("❌ ERREUR: Timeout - le serveur met trop de temps à répondre")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ ERREUR de requête: {e}")
        
    except Exception as e:
        print(f"❌ ERREUR inattendue: {e}")

if __name__ == "__main__":
    print("🚀 Script de test du module contact")
    print("=" * 60)
    
    # Vérifier que le module requests est installé
    try:
        import requests
    except ImportError:
        print("❌ Le module 'requests' n'est pas installé")
        print("💡 Installez-le avec: pip install requests")
        exit(1)
    
    test_contact_api()
    
    print("\n" + "=" * 60)
    print("✨ Test terminé!")
    print("📧 Si le test réussit, vous devriez recevoir un email dans quelques minutes.")
