""" Django settings for project project. """

import os
# from project.secrets import aws_secrets, config_secrets

SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.abspath(SETTINGS_DIR + "/../..")
GIT_DIR = os.path.abspath(PROJECT_DIR + "/..")

STATIC_ROOT = GIT_DIR + "/static/"
# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(PROJECT_DIR, "static")]

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


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False



DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

MEDIA_ROOT = GIT_DIR + "/media/"
MEDIA_URL = "/media/"

ALLOWED_HOSTS = ["facet-dev.elasticbeanstalk.com"]
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'editorial',
    'imagekit',
    'simple_history',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'bootstrap3_datetime',
    'tinymce',
    'project', # for custom management commands
    'storages', # for use with S3
)

SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
)

TINYMCE_JS_ROOT = '/static/scripts/tiny_mce/'
TINYMCE_JS_URL = os.path.join(STATIC_URL, 'scripts/tiny_mce/tinymce.min.js')
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "spellchecker,paste,searchreplace",
    'invalid_styles': 'position',
    'theme': "modern",
}
TINYMCE_SPELLCHECKER = True

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'project.context_processors.include_private_message_form',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_USER_MODEL = 'editorial.User'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_REDIRECT_URL = '/dashboard'

WSGI_APPLICATION = 'project.wsgi.application'

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'facet',
            'HOST': 'localhost',
            'PORT': '5432',
            'USER': 'facet',
            'PASSWORD': 'collaborate'
        }
    }


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True
