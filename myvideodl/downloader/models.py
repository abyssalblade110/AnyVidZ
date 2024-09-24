from django.db import models

class VideoDownload(models.Model):
    url = models.URLField(max_length=255)
    action = models.CharField(max_length=10, choices=[('download', 'Download'), ('convert', 'Convert')])
    quality = models.CharField(max_length=10, choices=[('best', 'Best'), ('worst', 'Worst')])
    timestamp = models.DateTimeField(auto_now_add=True)
