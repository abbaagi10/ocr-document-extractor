# 📄 AI-Powered Document Extractor (Full-Stack)

Une application Full-Stack asynchrone qui combine l'OCR (Tesseract) et l'IA générative (Google Gemini) pour extraire et structurer intelligemment les données de n'importe quel document ou facture.

## 🚀 Architecture Technique

Le projet repose sur une architecture moderne, entièrement conteneurisée :

*   **Frontend :** React, Vite, Tailwind CSS v4
*   **Backend API :** Python, Django, Django REST Framework
*   **Traitement Asynchrone :** Celery + Redis (Message Broker)
*   **Moteurs d'Extraction :** Tesseract OCR (texte brut) + Google Gemini 3.5 Flash (structuration JSON)
*   **Infrastructure :** Docker & Docker Compose

## ⚙️ Fonctionnalités clés

*   **Traitement Asynchrone :** L'interface React ne bloque jamais pendant l'analyse grâce à Celery et un système de polling intelligent.
*   **Extraction Intelligente :** Gemini analyse le texte brut issu de l'OCR pour renvoyer un objet JSON parfaitement structuré, même si le format de la facture change.
*   **Déploiement en 1 clic :** L'ensemble de la stack (base de données, broker, backend, frontend) se lance avec un seul fichier `docker-compose.yml`.

## 🛠️ Comment lancer le projet en local

1. Clonez ce dépôt :
```bash
git clone [https://github.com/abbaagi10/ocr-document-extractor.git](https://github.com/abbaagi10/ocr-document-extractor.git)
cd ocr-document-extractor