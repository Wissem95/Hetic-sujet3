.PHONY: install init-db run

install:
	@echo "Installation de PostgreSQL..."
	brew install postgresql@14
	brew services start postgresql@14
	@echo "Installation des dépendances Python..."
	cd backend && pip install flask flask-sqlalchemy flask-cors flask-migrate psycopg2-binary python-dotenv
	@echo "Installation terminée !"

init-db:
	@echo "Mise à jour de la base de données..."
	cd backend && flask db upgrade
	@echo "Base de données mise à jour !"

run:
	@echo "Lancement du serveur..."
	cd backend && python3 app.py