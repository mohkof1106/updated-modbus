"""
WSGI config for modbus_controller project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""


# https://community.webfaction.com/questions/8598/internal-server-error-with-django-app-cant-access-website
import sys
sys.path.insert(0, '/home/enerwhere/webapps/modbus_controller/modbus_controller')

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modbus_controller.settings")

application = get_wsgi_application()
