from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class BackupLog(models.Model):
    filename = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=50)
    backup_type = models.CharField(max_length=50)
    owner = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='backup_logs'
    )

    def __str__(self):
        return self.filename
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
