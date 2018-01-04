#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    try:
        # on production, try to load environmental secrets
        import env
    except ImportError:
        pass

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.development")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
