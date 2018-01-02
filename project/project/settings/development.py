"""Development settings for facet project."""

from django.conf import settings
from django.test.runner import DiscoverRunner
from django.core.mail.utils import DNS_NAME

from .base import *


SECRET_KEY = "abcdef"

DEBUG = True
ALLOWED_HOSTS = ['localhost']

INSTALLED_APPS += [
    'debug_toolbar',
]

INTERNAL_IPS = ["127.0.0.1"]

MIDDLEWARE_CLASSES += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


##############################################################################################
# Email
#
# We don't want to send real email, so just print to the console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Fix for broken DNS at some wifi hot-spots
DNS_NAME._fqdn = "localhost"


##############################################################################################
# Logging & Error Reporting

# Blather on about every little thing that happens. We programmers get lonely.

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         '': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#         },
#         'factory': {  # FactoryBoy is too chatty!
#             'handlers': ['console'],
#             'level': 'INFO',
#         },
#         'django.db.backends': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': False,
#         }
#
#     },
# }


##############################################################################################
# Caching --- don't actual cache

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}


##############################################################################################
# Testing
#
# We don't want to spray all sorts of factory-made fake media stuff in the media folder
# (it won't hurt things, but will take up space), so let's use the temp directory for that.


class MediaTempTestSuiteRunner(DiscoverRunner):
    def __init__(self, *args, **kwargs):
        settings.MEDIA_ROOT = "/tmp"
        super(MediaTempTestSuiteRunner, self).__init__(*args, **kwargs)


TEST_RUNNER = 'project.settings.development.MediaTempTestSuiteRunner'
