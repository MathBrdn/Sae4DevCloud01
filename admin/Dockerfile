# Utilisez une image Python officielle
FROM python:3.11-slim

# Éviter que Python n'écrive des fichiers .pyc et forcer l'affichage des logs en temps réel
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le dossier de travail dans le conteneur
WORKDIR /workspace

# Installer les dépendances système nécessaires (si besoin de compiler certains packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt /workspace/
RUN pip install --no-cache-dir -r requirements.txt

# Installer Gunicorn (le serveur de production pour Django)
RUN pip install gunicorn

# Copier le reste du code du projet
COPY . /workspace/

# Exposer le port interne du conteneur (on utilisera 8002 pour les trois en interne)
EXPOSE 8002

# Commande par défaut pour démarrer Django avec Gunicorn
# (Remplacez 'mon_projet' par le nom du dossier contenant votre wsgi.py)
CMD ["gunicorn", "--chdir", "/workspace", "admin.wsgi:application", "--bind", "0.0.0.0:8002"]
