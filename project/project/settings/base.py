"""Base settings for Facet. Development and Production inherit from this."""

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

MEDIA_ROOT = GIT_DIR + "/media/"
MEDIA_URL = "/media/"

ALLOWED_HOSTS = []
# Application definition

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

    # 'project',   # FIXME from WJB: normally, site proj not in installed_apps
]

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

TINYMCE_JS_ROOT = os.path.join(STATIC_URL, 'scripts/tiny_mce/')
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
                'django.core.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'project.context_processors.include_private_message_form',
                'project.context_processors.include_activity_stream',
                'project.context_processors.include_logged_in_users',
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

SERVER_EMAIL = DEFAULT_FROM_EMAIL = "facet-mail@example.com"

# -------------------------------------------------------------- #
# DJANGO REST FRAMEWORK #
# -------------------------------------------------------------- #

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# -------------------------------------------------------------- #
# ACTIVITY STREAM SETTINGS #
# -------------------------------------------------------------- #

ACTSTREAM_SETTINGS = {
    'MANAGER': 'editorial.managers.MyActionManager',
    'FETCH_RELATIONS': True,
    'USE_PREFETCH': True,
    'USE_JSONFIELD': True,
    'GFK_FETCH_DEPTH': 2,
}

# -------------------------------------------------------------- #
# OTHER SETTINGS #
# -------------------------------------------------------------- #


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
