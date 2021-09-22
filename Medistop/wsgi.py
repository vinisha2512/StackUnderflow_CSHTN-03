from dotenv import load_dotenv
"""
WSGI config for Medistop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Medistop.settings')

# adjust as appropriate
project_folder = os.path.expanduser(str(Path(__file__).resolve().parent.parent))
load_dotenv(os.path.join(project_folder, '.env'))
print(os.path.join(project_folder, '.env'))

application = get_wsgi_application()
