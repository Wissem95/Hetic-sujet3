# Projet API Météo - HETIC

## 📋 Description du Projet

Ce projet est une API météorologique développée dans le cadre du cours de développement backend à HETIC. L'application permet de gérer et visualiser les données météorologiques de différentes villes avec une interface utilisateur simple et intuitive.

## 🎯 Objectifs du Projet

- Création d'une API RESTful avec Flask
- Gestion d'une base de données PostgreSQL
- Implémentation d'un frontend en JavaScript Vanilla
- Gestion des performances et du Big Data
- Documentation technique complète

## 🛠️ Technologies Utilisées

### Backend
- Python 3.13
- Flask (Framework Web)
- PostgreSQL (Base de données)
- SQLAlchemy (ORM)
- Flask-Migrate (Migrations de base de données)

### Frontend
- HTML5
- CSS3
- JavaScript Vanilla

## 🏗️ Architecture du Projet 

weather_app/
├── backend/
│ ├── api/
│ │ └── weather_service.py (Service météo)
│ ├── models/
│ │ └── weather.py (Modèles de données)
│ ├── templates/ (Templates Flask)
│ ├── static/
│ │ └── swagger.yml (Documentation API)
│ ├── app.py (Application principale)
│ ├── config.py (Configuration)
│ └── .env (Variables d'environnement)
└── frontend/
├── css/
│ └── style.css (Styles)
├── js/
│ └── main.js (JavaScript)
└── index.html (Page principale)

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.13+
- PostgreSQL
- pip

### Installation

1. Cloner le repository
```
bash
git clone [URL_DU_REPO]
cd weather_app
``` 

2. Configurer la base de données PostgreSQL
```
bash
createdb weather_db
```

3. Installer les dépendances Python
```
bash
cd backend
pip3 install -r requirements.txt
```

4. Lancer l'application
```
bash
# Terminal 1 - Backend
cd backend
python3 app.py

# Ouvrir frontend/index.html dans un navigateur
```

## 📡 API Endpoints

### Endpoints Principaux
- `GET /api/health` - Vérification de l'état de l'API
- `POST /api/weather` - Ajouter des données météo
- `GET /api/weather/<city>` - Obtenir les données météo d'une ville
- `GET /api/weather/<city>/history` - Obtenir l'historique météo
- `GET /api/weather/<city>/stats` - Obtenir les statistiques météo

### Exemple de Requête
```bash
curl -X POST http://127.0.0.1:5000/api/weather \
-H "Content-Type: application/json" \
-d '{
  "city": "Paris",
  "temperature": 20.5,
  "humidity": 65,
  "description": "Ensoleillé"
}'
```

## 💾 Structure de la Base de Données

### Table: weather_data
- id (PK)
- city
- temperature
- humidity
- description
- timestamp

## 🔍 Fonctionnalités Principales

### Backend
- API RESTful complète
- Gestion de base de données PostgreSQL
- Validation des données
- Gestion des erreurs
- Documentation Swagger

### Frontend
- Interface utilisateur responsive
- Affichage des données en temps réel
- Formulaire d'ajout de données
- Visualisation de l'historique
- Statistiques par ville

## 👥 Auteur

- Wissem BALI
- Formation : HETIC
- Projet : Sujet 3 - API Météo

## 📈 Améliorations Futures Possibles

- Ajout d'authentification
- Cache des données
- Tests unitaires
- Déploiement sur un serveur de production
- Interface d'administration

## 📄 Licence

Ce projet est réalisé dans le cadre d'un cours à HETIC.
```


