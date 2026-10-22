# core/celery.py
import os
from celery import Celery

# Définit le module de paramètres par défaut de Django pour le programme 'celery'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Lit la configuration depuis les paramètres Django (les variables commençant par CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Demande à Celery de chercher automatiquement les fichiers tasks.py dans nos applications
app.autodiscover_tasks()