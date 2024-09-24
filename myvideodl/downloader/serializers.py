from rest_framework import serializers
from .models import VideoDownload

class VideoDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoDownload
        fields = '__all__'
