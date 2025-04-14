# backup_manager/management/commands/export_backup.py
import os
import zipfile
import datetime
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Export DB and media folder into a zip archive"

    def handle(self, *args, **options):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = os.path.join(settings.BASE_DIR, "backups")
        os.makedirs(backup_dir, exist_ok=True)

        db_file = os.path.join(backup_dir, f"db_{timestamp}.json")
        media_dir = settings.MEDIA_ROOT
        zip_file = os.path.join(backup_dir, f"site_backup_{timestamp}.zip")

        os.system(f"python manage.py dumpdata --exclude sessions --indent 2 > {db_file}")

        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(db_file, os.path.basename(db_file))
            for root, dirs, files in os.walk(media_dir):
                for file in files:
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, media_dir)
                    zipf.write(abs_path, os.path.join("media", rel_path))

        os.remove(db_file)
        self.stdout.write(self.style.SUCCESS(f"Backup created: {zip_file}"))

