""" Development settings for facet project. """

from .settings import *

# -------------------------------------------------------------- #
# KEYS #
# -------------------------------------------------------------- #

# SECURITY WARNING: keep the secret key used in production secret!

# FIXME: Uggo, but makes it so you know everything you haven't set without
# needing to connect to aws each time. 

unset_secrets = False

if 'SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['SECRET_KEY']
else:
    print "You haven't set your Django SECRET_KEY. Use `$ python manage.py generatekey` to generate one. "
    unset_secrets = True

if 'AWS_STORAGE_BUCKET_NAME' in os.environ:
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
else:
    print "You haven't set your AWS_STORAGE_BUCKET_NAME"
    unset_secrets = True

if 'AWS_ACCESS_KEY_ID' in os.environ:
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
else:
    print "You haven't set your AWS_ACCESS_KEY_ID"
    unset_secrets = True

if 'AWS_SECRET_ACCESS_KEY' in os.environ:
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
else:
    print "You haven't set your AWS_SECRET_ACCESS_KEY"
    unset_secrets = True

if unset_secrets:
    raise KeyError, "There are unset keys. Use `$ eb setenv KEY=value` to set."

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

TINYMCE_JS_ROOT = os.path.join(STATIC_URL, 'scripts/tiny_mce/')
TINYMCE_JS_URL = os.path.join(STATIC_URL, 'scripts/tiny_mce/tinymce.min.js')

# -------------------------------------------------------------- #
# MODULES #
# -------------------------------------------------------------- #

INSTALLED_APPS = INSTALLED_APPS + (
    'storages', # for use with S3
)

# -------------------------------------------------------------- #
# DEBUGGING #
# -------------------------------------------------------------- #

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# -------------------------------------------------------------- #
# S3 FILE STORAGE #
# -------------------------------------------------------------- #

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# -------------------------------------------------------------- #
# APPLICATION DEFINITION? #
# -------------------------------------------------------------- #

ALLOWED_HOSTS = [
    "facet-katie-dev.us-west-1.elasticbeanstalk.com",
    "facet-dev.us-west-1.elasticbeanstalk.com",
    "facet-production.us-west-1.elasticbeanstalk.com",
    "demo.projectfacet.com"
    ]

# -------------------------------------------------------------- #
# DATABASE #
# -------------------------------------------------------------- #

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('RDS_DB_NAME', 'facet'),
        'USER': os.environ.get('RDS_USERNAME', 'localhost'),
        'PASSWORD': os.environ.get('RDS_PASSWORD', 5432),
        'HOST': os.environ.get('RDS_HOSTNAME', 'facet'),
        'PORT': os.environ.get('RDS_PORT', 'collaborate'),
    }
}

# Are these RDS_* keys predetermined by Amazon?
# TODO remove below once above is answered

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.environ.get('PD_DB','facet'),
#         'HOST': os.environ.get('PD_HOST', 'localhost'),
#         'PORT': os.environ.get('PD_PORT', 5432),
#         'USER': os.environ.get('PD_USER', 'facet'),
#         'PASSWORD': os.environ.get('PD_PW', 'collaborate'),
#     }
# }


