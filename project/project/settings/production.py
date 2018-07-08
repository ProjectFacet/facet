"""Production settings for facet project."""

from .base import *

##############################################################################
# Core Django stuff

SECRET_KEY = os.environ['SECRET_KEY']

INSTALLED_APPS += [
    #'storages',  # for use with S3
    "dbbackup",
]

DEBUG = False

ALLOWED_HOSTS = ['projectfacet.com']

######################################
# Database: local PostgreSQL

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'facet'),
        'USER': os.environ.get('DB_USERNAME', 'facet'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'collaborate'),
        'HOST': os.environ.get('DB_HOSTNAME', 'localhost'),
        'PORT': os.environ.get('DB_PORT', 5432),
        'CONN_MAX_AGE': 600,
    }
}

######################################
# Logging & Error Reporting

# By default, we write reasonably important things (INFO and above) to the console
# We email admins on a site error or a security issue and also propagate
# this up to the Heroku logs. This is obviously overridden in the development settings.

LOGGING = {
    'disable_existing_loggers': False,
    'version': 1,

    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'WARNING',
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['console', 'mail_admins'],
            'level': 'WARNING',
            'propagate': True,
        },
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

######################################
# Template Loaders
#
# Performance improvement; template changes not effective until the process is restarted.

TEMPLATES[0]['OPTIONS']['loaders'] = [
    ('django.template.loaders.cached.Loader',
     ('django.template.loaders.filesystem.Loader',
      'django.template.loaders.app_directories.Loader')
     )
]
del TEMPLATES[0]['APP_DIRS']

##############################################################################
# 3rd Party Products

######################################
# Store static/media at S3

# Not storing things at S3 at this time; will explore later

# AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
# AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# AWS_S3_CUSTOM_DOMAIN = AWS_STORAGE_BUCKET_NAME + '.s3.amazonaws.com'

#STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

# -------------------------------------------------------------- #
# EMAIL #
# -------------------------------------------------------------- #

# shouldn't need with current django/common AWS setup
# EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'

EMAIL_HOST = 'email-smtp.us-west-2.amazonaws.com'
EMAIL_HOST_USER = os.environ['AWS_EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['AWS_EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True
# WJB: unsure what this would be for, commented out for now
# AWS_SES_REGION_ENDPOINT = 'email-smtp.us-west-2.amazonaws.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL = "collaborate@projectfacet.org"


##############################################################################################
# Backups
#
# We use django-dbbackup; this makes a pgdump and a zip of the media directory.
# It needs cron to call it, so there's a cron installed for the site on the server.
# See conf/ for the the setup for that.
#
# Separate from this, the cron copies things to Joel's S3 account for off-server
# storage. Paranoia FTW!

DBBACKUP_STORAGE = "django.core.files.storage.FileSystemStorage"
DBBACKUP_STORAGE_OPTIONS = {'location': GIT_DIR + '/backups/'}
HOSTNAME = "projectfacet.com"
DBBACKUP_CLEANUP_KEEP = 3
DBBACKUP_CLEANUP_KEEP_MEDIA = 3
