"""Staging setup.

For this project, "staging" means "running on dev environment, but with caching and such set
up like production."

This will use the static/media on S3 -- so don't casually add/change assets for real orgs!
The database itself is local, though.
"""

from django.core.mail.utils import DNS_NAME

from .production import *

# Can visit site as http://localhost or with fake URL http://facet.staging (assuming your
# computer will interpret that name to where the staging server is!)
ALLOWED_HOSTS = ['localhost', 'facet.staging']

MIDDLEWARE += [
    'project.timing.TimingMiddleware',
]

##############################################################################################
# Email
#
# We don't want to send real email, so just print to the console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

##############################################################################################
# Logging & Error Reporting
#
# Be moderately chatty

LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.db': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    },
}