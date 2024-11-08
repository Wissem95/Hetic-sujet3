.PHONY: install init-db run

install:
	@echo "Installation des dépendances..."
	cd backend && pip install flask flask-sqlalchemy flask-cors flask-migrate
	cd backend && pip install -r requirements.txt
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