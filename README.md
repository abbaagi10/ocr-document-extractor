# 📄 OCR Document Extractor API

Une API backend complète conçue pour l'extraction asynchrone et la structuration de données à partir de documents complexes (PDF, images), utilisant des techniques de vision par ordinateur et d'OCR.

## 🚀 Fonctionnalités
* **Prétraitement visuel :** Nettoyage des images, binarisation adaptative et redressement (Deskewing) via OpenCV.
* **Extraction OCR :** Reconnaissance optique de caractères via Tesseract/PaddleOCR.
* **Structuration des données :** Parsing du texte brut en format JSON exploitable.
* **Architecture Asynchrone :** API non bloquante avec Django REST Framework, Celery et Redis.

## 🛠️ Stack Technique
* **Backend :** Python 3.10, Django, Django REST Framework
* **IA & Vision :** OpenCV, PyTesseract
* **Asynchronisme :** Celery, Redis
* **Déploiement :** Docker, Docker Compose

## 🐳 Démarrage Rapide (Docker)

1. Clonez le dépôt :
   ```bash
   git clone [https://github.com/votre-nom/ocr-document-extractor.git](https://github.com/votre-nom/ocr-document-extractor.git)
   cd ocr-document-extractor