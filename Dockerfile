FROM swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/python:3.10-slim

# Empêche Python d'écrire des fichiers .pyc et force l'affichage des logs dans le terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installation des dépendances système critiques
# libgl1-mesa-glx et libglib2.0-0 sont obligatoires pour OpenCV
# tesseract-ocr et tesseract-ocr-fra installent le moteur OCR et la langue française
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    tesseract-ocr \
    tesseract-ocr-fra \
    && rm -rf /var/lib/apt/lists/*

# Définition du répertoire de travail dans le conteneur
WORKDIR /app

# Copie des dépendances et installation
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copie du reste du code source
COPY . /app/