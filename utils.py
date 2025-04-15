import os
import zipfile
import datetime
from django.conf import settings


def generate_backup(command_shell_obj = None):
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
    
    if command_shell_obj is not None:
        command_shell_obj.stdout.write(command_shell_obj.style.SUCCESS(f"Backup created: {zip_file}"))

