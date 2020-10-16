from django.core.management.base import BaseCommand
from snow_camera.services.location_parser import SnowLocationParser


class Command(BaseCommand):
    help = 'remove stop word duplicates'

    def add_arguments(self, parser):
        parser.add_argument('--dry_run', dest='dry_run', action='store_true')

    def handle(self, *args, **options):
        SnowLocationParser().run()
