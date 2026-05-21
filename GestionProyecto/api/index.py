import os
import sys

# Apunta al directorio raiz del proyecto (GestionProyecto/)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'antigravity.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Vercel requiere la variable llamada 'app'
app = application
