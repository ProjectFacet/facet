""" Development settings for facet project. """

from .settings import *

from django.core.mail.utils import DNS_NAME


INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
)

DEBUG = True

##############################################################################################
# Email
#
# We don't want to send real email, so just print to the console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Fix for broken DNS at some wifi hot-spots
DNS_NAME._fqdn = "localhost"