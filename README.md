# Application Météo

Application web de météo avec base de données pré-remplie pour 70 villes.

## Prérequis

1. Installer Homebrew (macOS):

bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2. Installer Python avec Homebrew:

bash
brew install python

3. Vérifier l'installation:

bash
python --version  # Doit afficher Python 3.x.x

## Installation

1. Cloner le projet:

bash
git clone https://github.com/Wissem95/hetic-sujet3.git

cd hetic-sujet3
cd weather_app

2. Installer les dépendances:

bash
-Installer les dépendances

make install

-Initialiser la base de données

make init-db

-Lancer le serveur

make run


4. Ouvrir le frontend:
Allez sur http://localhost:5000 ou http://127.0.0.1:5000

## Structure
```
weather_app/
├── backend/
│   ├── migrations/     # Migrations DB
│   ├── models/        # Modèles
│   ├── api/          # Routes API
│   ├── weather.db    # Base de données (pré-remplie)
│   └── app.py       # Application Flask
└── frontend/
    ├── css/
    ├── js/
    └── index.html
```

## Fonctionnalités
- Météo actuelle avec icônes
- Historique des données
- Statistiques et analyses
- Auto-complétion des villes
- Base de données déjà remplie avec:
  - 10 villes tunisiennes
  - 10 villes françaises
  - 10 villes belges
  - 10 villes italiennes
  - 10 villes espagnoles
  - 10 villes portugaises
  - 10 villes anglaises

## API
- GET /api/weather/<city> : Météo actuelle
- GET /api/weather/<city>/history : Historique
- GET /api/weather/<city>/stats : Statistiques
- POST /api/weather : Ajout de données

## Base de données
La base de données SQLite est déjà configurée et remplie avec toutes les données météo.
Aucune configuration supplémentaire n'est nécessaire.
```
