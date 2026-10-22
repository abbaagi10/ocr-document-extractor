# extractor/models.py
import uuid
from django.db import models

class Document(models.Model):
    # Utilisation d'un UUID pour plus de sécurité (au lieu d'un ID 1, 2, 3...)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # L'image sera sauvegardée dans un dossier 'media/documents/'
    image = models.ImageField(upload_to='documents/')
    
    # Statut du traitement asynchrone
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('processing', 'En cours de traitement'),
        ('completed', 'Terminé'),
        ('error', 'Erreur'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Le texte brut extrait par Tesseract
    extracted_text = models.TextField(blank=True, null=True)
    
    # Le texte structuré en JSON (pour aller plus loin plus tard)
    structured_data = models.JSONField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.id} - {self.status}"