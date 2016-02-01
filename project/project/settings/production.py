""" Development settings for facet project. """

from .settings import *

SECRET_KEY = os.environ['SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('PD_DB','facet'),
        'HOST': os.environ.get('PD_HOST', 'localhost'),
        'PORT': os.environ.get('PD_PORT', 5432),
        'USER': os.environ.get('PD_USER', 'facet'),
        'PASSWORD': os.environ.get('PD_PW', 'collaborate'),
    }
}
