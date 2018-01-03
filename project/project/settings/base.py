"""Base settings for Facet. Development and Production inherit from this."""

import os

# Directories used in these settings files
SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_DIR = os.path.abspath(SETTINGS_DIR + "/../..")
GIT_DIR = os.path.abspath(PROJECT_DIR + "/..")

##############################################################################
# Core Django stuff

WSGI_APPLICATION = 'project.wsgi.application'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'bootstrap3',
    'imagekit',
    'editorial.apps.EditorialAppConfig',
    'simple_history',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'rest_framework',
    'allauth.socialaccount',
    'bootstrap3_datetime',
    'tinymce',
    'watson',
    'embed_video',
    'actstream',
]

SITE_ID = 1

# Be cautious about adding things here; the order can be important
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'project.urls'

#######################################
# Database: local Postgres

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'facet',
        'HOST': 'localhost',
        'USER': 'facet',
        'PASSWORD': 'collaborate'
    }
}

#######################################
# Localization / Time

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#######################################
# Static files / Media files

STATIC_ROOT = GIT_DIR + "/static/"
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(PROJECT_DIR, "static")]

MEDIA_ROOT = GIT_DIR + "/media/"
MEDIA_URL = "/media/"

#######################################
# Django templates

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
                'project.context_processors.include_activity_stream',
                'project.context_processors.include_logged_in_users',
            ],
        },
    },
]

#######################################
# Auth: add in allauth stuff

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_USER_MODEL = 'editorial.User'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
LOGIN_REDIRECT_URL = '/dashboard'

#######################################
# Email

SERVER_EMAIL = DEFAULT_FROM_EMAIL = "facet-mail@example.com"

# Email these people when errors happen on production sites

ADMINS = [
    ('Joel', 'joel@joelburton.com'),
    ('Meggie', 'meggie@hackbrightacademy.com'),
    ('Jessica', 'jessica@hackbrightacademy.com'),
]

######################################
# Sessions
#
# We don't need any server-side storage of sessions, so just use cookies

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

##############################################################################
# 3rd Party Products

######################################
# ImageKit (Django app for resizing image fields)

# Be optimistic, produce URLs for images that may not exist.
#
# This is helpful as it means we don't need to have a media file on the development/staging
# server in order to show a view that uses it. It will optimistically make the URL, hoping
# it is there. This does mean that when you add/change an ImageKit field, you need to
# regenerate the images with ``python manage.py generateimages``

IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'imagekit.cachefiles.strategies.Optimistic'

#######################################
# Django REST Freamework

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

#######################################
# Activity Stream

ACTSTREAM_SETTINGS = {
    'MANAGER': 'editorial.managers.MyActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 2,
}

#######################################
# TinyMCE (HTML widget)

TINYMCE_JS_ROOT = os.path.join(STATIC_URL, 'scripts/tiny_mce/')
TINYMCE_JS_URL = os.path.join(STATIC_URL, 'scripts/tiny_mce/tinymce.min.js')
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "spellchecker,paste,searchreplace,wordcount",
    'invalid_styles': 'position',
    'theme': "modern",
}
TINYMCE_SPELLCHECKER = True
