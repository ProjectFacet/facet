from django.utils.crypto import get_random_string
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
    	""" generate a new SECRET_KEY a la Django's startproject """
    	
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!#$%^&*()'
        print get_random_string(50, chars)