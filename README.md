install.bat (Windows)
@echo off

rem Créer l'environnement virtuel
python -m venv env
call env\Scripts\activate

rem Installer les dépendances
pip install django

rem Créer le projet Django
django-admin startproject myproject
cd myproject

rem Créer la base de données SQLite3
python manage.py migrate
python manage.py createsuperuser

rem Lancer le serveur de développement
python manage.py runserver

install.ps1 (PowerShell)
# Créer l'environnement virtuel
python -m venv env
. .\env\Scripts\Activate.ps1

# Installer les dépendances
pip install django

# Créer le projet Django
django-admin startproject myproject
cd myproject

# Créer la base de données SQLite3
python manage.py migrate
python manage.py createsuperuser

# Lancer le serveur de développement
python manage.py runserver

install.sh (Linux/macOS)
#!/bin/bash

# Créer l'environnement virtuel
python3 -m venv env
source env/bin/activate

# Installer les dépendances
pip install django

# Créer le projet Django
django-admin startproject myproject
cd myproject

# Créer la base de données SQLite3
python3 manage.py migrate
python3 manage.py createsuperuser

# Lancer le serveur de développement
python3 manage.py runserver
