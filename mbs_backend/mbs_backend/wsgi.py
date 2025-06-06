"""
WSGI config for mbs_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set API URL environment variable
os.environ.setdefault('API_URL', 'http://localhost:8000/api')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mbs_backend.settings')

application = get_wsgi_application()
