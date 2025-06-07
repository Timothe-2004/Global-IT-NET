#!/bin/bash

# Installer les dépendances
pip install -r requirements.txt

# Exécuter les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --noinput
