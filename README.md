# P9 - Développer une application web en utilisant Django

### But

- Demander des critiques de livres ou d'articles en créant des tickets
- Lire des critiques de livre ou d'article
- Publier des critiques de livres ou d'articles
- Maintenir une interface utilisateur simple et minimaliste

### Caractéristiques

# Authentification

Les utilisateurs peuvent se connecter, se déconnecter et s'inscrire.
Les utilisateurs non authentifiés ne peuvent accéder qu'aux pages de connexion et d'inscription.

# Tickets (demande de révision d'un utilisateur)

- L'utilisateur peut demander une critique pour un livre ou des articles
- Les abonnés de l'utilisateur peuvent publier des avis en réponse
- L'utilisateur peut créer un ticket et un avis simultanément

# Flux (page d'accueil)

Le flux affiche les éléments suivants dans l'ordre chronologique inverse :

- Tous les tickets et avis des utilisateurs suivis par l'utilisateur
- Tous les billets et avis de l'utilisateur
- Avis en réponse aux tickets de l'utilisateur par les abonnés de l'utilisateur (même si l'utilisateur ne les suit pas)
- Possibilité de créer un ticket pour demander un avis
- Possibilité de créer un avis
- Possibilité de créer un ticket et un avis en même temps
- Possibilité d'afficher, de modifier et de supprimer ses propres billets et avis

# abonnements

Un utilisateur peut suivre d'autres utilisateurs pour voir leurs demandes et critiques.
Les utilisateurs peuvent rechercher des noms d'utilisateur pour les suivre.
Il existe une page répertoriant tous les utilisateurs qu'un utilisateur suit et tous les utilisateurs qui le suivent.
Un utilisateur peut ne plus suivre un autre utilisateur.
Un utilisateur peut bloquer un autre utilisateur.

### Spécifications techniques

- Utiliser Django
- Utiliser SQLite3
- avoir une interface compatible WCAG
- être conforme à PEP8

### Comment lancer l'application ?

- Installez Python 3.12. Lancez la console et, dans le dossier de votre choix, clonez ce dépôt :

```
clone git https://github.com/projets-openclassrooms/Projet9_Web_Django.git
```

- Dans le dossier, créez et activez un nouvel environnement virtuel :

```
(Linux)
python3 -m venv .venv
source .venv/bin/activate
(les fenêtres)
python -m venv .venv
.\.venv\Scripts\activate
```

- Ensuite, installez les packages requis :

```
pip install -r requirements.txt
```

```
python manage.py makemigrations
```

```
python manage.py migrate
```
```
python manage.py createsuperuser
```

Ceci, afin d'ajouter un admin de la base

- Enfin, lancez le serveur :

```

python manage.py runserver 8000
```

Vous pouvez désormais accéder à cette application sur http://127.0.0.1:8000