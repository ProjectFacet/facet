""" Development settings for facet project. """

from .settings import *

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
    'project', # for custom management commands
    'storages', # for use with S3
)