try:
    from django.contrib.sessions.management.commands.clearsessions import Command  # flake8: noqa
except ImportError:
    pass  # not supported on Django 1.4
