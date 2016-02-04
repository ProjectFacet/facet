""" Development settings for facet project. """

from .settings import *

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
    'storages', # for use with S3
)