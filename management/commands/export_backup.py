from django.core.management.base import BaseCommand
from ...utils import generate_backup

class Command(BaseCommand):
    help = "Export DB and media folder into a zip archive"

    def handle(self, *args, **options):
        generate_backup(self)

