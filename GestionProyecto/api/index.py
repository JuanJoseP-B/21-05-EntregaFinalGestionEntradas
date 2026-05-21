import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'antigravity.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from django.core.management import call_command
call_command('migrate', verbosity=1)

app = application
