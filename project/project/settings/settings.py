""" Base settings for Facet. Development and Production inherit from this. """

import os

# -------------------------------------------------------------- #
# DIRECTORIES
# -------------------------------------------------------------- #

SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.abspath(SETTINGS_DIR + "/../..")
GIT_DIR = os.path.abspath(PROJECT_DIR + "/..")

STATIC_ROOT = GIT_DIR + "/static/"
# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(PROJECT_DIR, "static")]

# -------------------------------------------------------------- #
# EMAIL #
# -------------------------------------------------------------- #

# SECURITY WARNING: keep the secret key used in production secret!
# Dev purposes only, will be replaced...
SECRET_KEY = os.environ['SECRET_KEY']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MEDIA_ROOT = GIT_DIR + "/media/"
MEDIA_URL = "/media/"

ALLOWED_HOSTS = []
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'editorial.apps.EditorialAppConfig',
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
    'watson',
    'project'
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
    'plugins': "spellchecker,paste,searchreplace,wordcount",
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

# -------------------------------------------------------------- #
# EMAIL #
# -------------------------------------------------------------- #

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True

SERVER_EMAIL = os.environ['EMAIL_HOST_USER']
DEFAULT_FROM_EMAIL = os.environ['EMAIL_HOST_USER']


LOGIN_REDIRECT_URL = '/dashboard'

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'facet',
        'HOST': 'localhost',
        'USER': 'facet',
        'PASSWORD': 'collaborate'
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True
