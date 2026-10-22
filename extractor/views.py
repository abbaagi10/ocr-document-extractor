# extractor/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from .tasks import process_document_task

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by('-created_at')
    serializer_class = DocumentSerializer

    def create(self, request, *args, **kwargs):
        # 1. Validation et sauvegarde de l'image
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = serializer.save()

        # 2. Changement du statut
        document.status = 'processing'
        document.save()

        # 3. Déclenchement de la tâche asynchrone Celery
        # .delay() envoie la tâche dans Redis sans bloquer le serveur web
        process_document_task.delay(str(document.id), document.image.path)

        # 4. On répond immédiatement à l'utilisateur (Code HTTP 202: Accepted)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED, headers=headers)