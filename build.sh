#!/bin/bash

# Installer les dépendances
pip install -r requirements.txt

# Exécuter les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Créer automatiquement un superuser si aucun n'existe
python manage.py create_superuser_if_none_exists
