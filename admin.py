# backup_manager/admin.py
from django.contrib import admin
from django.http import HttpResponseRedirect, FileResponse
from django.urls import path
from django.contrib import messages
from .models import BackupLog
import os
from django.conf import settings

from my_backup.utils import generate_backup


class PermissionHandler:
    @staticmethod
    def has_permission(request):
        # Check if the user is a superuser
        if not request.user.is_superuser:
            messages.error(request, "You do not have permission to perform this action.")
            return False

        # Check if DEBUG is enabled
        if not settings.DEBUG:
            messages.error(request, "Backup functionality is disabled in production mode.")
            return False

        return True
    

@admin.register(BackupLog)
class BackupLogAdmin(admin.ModelAdmin):
    list_display = ("filename", "backup_type", "status", "owner", "created_at")
    readonly_fields = ("created_at", "updated_at")
    change_list_template = "admin/backup_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("generate-backup/", self.admin_site.admin_view(self.generate_backup), name="generate_backup"),
            path("download-latest/", self.admin_site.admin_view(self.download_latest), name="download_latest_backup"),
        ]
        return custom_urls + urls

    def has_permission(self, request):
        return PermissionHandler.has_permission(request)
    
    def generate_backup(self, request):
        if not self.has_permission(request):
            return HttpResponseRedirect("../")

        try:
            generate_backup()
            messages.success(request, "Backup created successfully.")
        except Exception as e:
            messages.error(request, f"Backup failed: {e}")
        return HttpResponseRedirect("../")

    def download_latest(self, request):
        if not self.has_permission(request):
            return HttpResponseRedirect("../")

        backup_dir = os.path.join(settings.BASE_DIR, "backups")
        if not os.path.exists(backup_dir):
            messages.error(request, "No backup directory found.")
            return HttpResponseRedirect("../")

        files = [f for f in os.listdir(backup_dir) if f.endswith(".zip")]
        if not files:
            messages.error(request, "No backup zip file found.")
            return HttpResponseRedirect("../")

        latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(backup_dir, f)))
        filepath = os.path.join(backup_dir, latest_file)
        return FileResponse(open(filepath, "rb"), as_attachment=True, filename=latest_file)