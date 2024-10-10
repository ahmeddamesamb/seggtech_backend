# Utiliser l'image Python 3.10 comme image de base
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application dans le conteneur
COPY . .

# Commande pour démarrer le serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
