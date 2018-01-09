"""Demo setup.

For this project, "demo" means "like production, but using an alternate db and not sending
real mail."
"""

from django.core.mail.utils import DNS_NAME

from .production import *

# Can visit site as http://localhost or with fake URL http://facet.staging (assuming your
# computer will interpret that name to where the staging server is!)
ALLOWED_HOSTS = ['demo.projectfacet.com']


##############################################################################################
# Email
#
# We don't want to send real email, so just print to the console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


######################################
# Database: local PostgreSQL

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'facet-demo'),
        'USER': os.environ.get('DB_USERNAME', 'facet'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'collaborate'),
        'HOST': os.environ.get('DB_HOSTNAME', 'localhost'),
        'PORT': os.environ.get('DB_PORT', 5432),
        'CONN_MAX_AGE': 600,
    }
}
