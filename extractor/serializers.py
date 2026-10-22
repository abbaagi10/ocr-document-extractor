# extractor/serializers.py
from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'image', 'status', 'extracted_text', 'structured_data', 'created_at']
        # On empêche l'utilisateur de modifier ces champs manuellement lors de l'upload
        read_only_fields = ['id', 'status', 'extracted_text', 'structured_data', 'created_at']