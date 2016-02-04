""" Development settings for facet project. """

from .settings import *
from .production import *

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
)

DEBUG = True