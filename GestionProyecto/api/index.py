import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'antigravity.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from django.core.management import call_command
try:
    call_command('migrate', verbosity=0)
except Exception as e:
    print(f"[MIGRATE ERROR] {e}", file=sys.stderr)

app = application
