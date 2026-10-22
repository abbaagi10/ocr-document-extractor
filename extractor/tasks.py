# extractor/tasks.py
import os
import json
import logging
from celery import shared_task
import cv2
import pytesseract
import google.generativeai as genai
from .models import Document

logger = logging.getLogger(__name__)

# Configuration de l'API IA
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

@shared_task(bind=True)
def process_document_task(self, document_id, image_path):
    logger.info(f"Début du traitement pour le document ID: {document_id}")
    
    try:
        document = Document.objects.get(id=document_id)
        
        # 1. Prétraitement avec OpenCV
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise ValueError("Impossible de lire l'image.")

        _, processed_image = cv2.threshold(
            image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        
        # 2. Extraction du texte (Tesseract)
        # On enlève lang='fra' pour qu'il lise l'anglais et le français par défaut
        extracted_text = pytesseract.image_to_string(processed_image)
        
        # 3. Structuration intelligente avec l'IA (LLM)
        structured_data = {}
        
        if api_key and extracted_text.strip():
            # Le prompt (les instructions) pour l'IA
            prompt = f"""
            Tu es un assistant spécialisé dans l'extraction de données comptables et administratives.
            Lis le texte OCR suivant, déduis de quel type de document il s'agit, et extrais les informations clés.
            
            Règles strictes :
            - Renvoie UNIQUEMENT un objet JSON valide, sans balises markdown (```json), sans texte avant ou après.
            - Les clés du JSON doivent être en minuscules (ex: type_document, emetteur, date, montant_total, identifiants).
            - Si une information n'est pas trouvée, mets la valeur à null.
            
            Texte OCR à analyser :
            {extracted_text}
            """
            
            # Utilisation du modèle de nouvelle génération disponible sur votre clé
            model = genai.GenerativeModel('gemini-3.5-flash')
            response = model.generate_content(prompt)
            
            try:
                # Nettoyage de la réponse pour s'assurer que c'est du JSON pur
                clean_json = response.text.replace("```json", "").replace("```", "").strip()
                structured_data = json.loads(clean_json)
            except json.JSONDecodeError:
                logger.error("L'IA n'a pas renvoyé un JSON valide.")
                structured_data = {"erreur": "Format JSON invalide depuis l'IA", "brut": response.text}

        # 4. Sauvegarde en BDD
        document.extracted_text = extracted_text.strip()
        document.structured_data = structured_data
        document.status = 'completed'
        document.save()
        
        logger.info(f"Traitement terminé avec succès pour {document_id}")
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Erreur pour {document_id}: {str(e)}")
        try:
            doc_error = Document.objects.get(id=document_id)
            doc_error.status = 'error'
            doc_error.save()
        except Document.DoesNotExist:
            pass
        return {"status": "error", "message": str(e)}