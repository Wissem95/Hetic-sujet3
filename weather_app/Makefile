.PHONY: install init-db run

install:
	@echo "Installation de PostgreSQL..."
	brew install postgresql@14
	brew services start postgresql@14
	@echo "Installation des dépendances Python..."
	cd backend && pip install flask flask-sqlalchemy flask-cors flask-migrate psycopg2-binary python-dotenv
	@echo "Installation terminée !"


run:
	@echo "Lancement du serveur..."
	cd backend && python3 app.py