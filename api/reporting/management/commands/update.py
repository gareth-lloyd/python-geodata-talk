from django.core.management.base import BaseCommand

from reporting import api

class Command(BaseCommand):
    args = ''
    help = 'Update all'

    def handle(self, *args, **options):
        pass
