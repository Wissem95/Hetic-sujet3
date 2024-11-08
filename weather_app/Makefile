.PHONY: install init-db run

install:
	@echo "Installation de PostgreSQL..."
	brew install postgresql@15
	brew services start postgresql@15
	@echo "Installation des dépendances Python..."
	cd backend && pip install flask flask-sqlalchemy flask-cors flask-migrate psycopg2-binary python-dotenv
	@echo "Installation terminée !"

init-db:
	@echo "Initialisation de la base de données..."
	cd backend && flask db init
	cd backend && flask db migrate -m "Initial migration"
	cd backend && flask db upgrade
	@echo "Base de données initialisée !"

run:
	@echo "Lancement du serveur..."
	cd backend && python app.py