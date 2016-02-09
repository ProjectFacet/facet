from django.core.management.base import BaseCommand
from random import choice, randrange


class Command(BaseCommand):

    def handle(self, *args, **options):
        """ creates a password between 12 and 20 characters in length """

        password = ""
        try:
            with open("/usr/share/dict/words") as wordfile:
                words = wordfile.read().lower().split()
                words = [word for word in words if len(word) < 6]
            while len(password) < 12:
                password += choice(words)
                if len(password) > 20:
                    password = ""

                
        except OSError:
            fodder = string.ascii_uppercase + string.ascii_lowercase + string.digits
            password = ''.join(choice(fodder) for _ in range(12))

        print password

                 

