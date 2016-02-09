from django.core.management.base import BaseCommand
from editorial.models import User
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        """ create a superuser for deployment """
        if not User.objects.filter(username="admin").exists():

            if 'ADMIN_PASSWORD' in os.environ:
                admin_password = os.environ['ADMIN_PASSWORD']
            else:
                error_string = "You have not set your ADMIN_PASSWORD. Use `$ python manage.py generatepass` to generate one. Use `$ eb setenv KEY=value` to set."
                raise KeyError, error_string

            User.objects.create_superuser('admin', 'admin@admin.com', admin_password)