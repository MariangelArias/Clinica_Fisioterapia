"""
WSGI config for fisioterapia_web project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

try:
	from django.core.wsgi import get_wsgi_application
except Exception as e:
	raise ImportError(
		"Couldn't import Django's WSGI application. Make sure Django is installed "
		"and available in your PYTHONPATH environment. Original error: {}".format(e)
	)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fisioterapia_web.settings')

application = get_wsgi_application()
