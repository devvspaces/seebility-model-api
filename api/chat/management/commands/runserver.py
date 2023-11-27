from django.core.management.commands.runserver import Command as runserver
from decouple import config


class Command(runserver):
    default_port = config("PORT", default="8000")
