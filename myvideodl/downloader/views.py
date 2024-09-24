from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import VideoDownload
from .serializers import VideoDownloadSerializer
import yt_dlp
import os
from django.http import Http404
from django.urls import reverse
from django.views import View
from django.http import HttpResponse

class VideoDownloadViewSet(viewsets.ModelViewSet):
    queryset = VideoDownload.objects.all()
    serializer_class = VideoDownloadSerializer

    @action(detail=False, methods=['post'])
    def download(self, request):
        url = request.data.get('url')
        action = request.data.get('action')
        quality = request.data.get('quality', 'best')

        # Download the video
        file_path = download_video(url, quality=quality, convert_to_mp3=(action == 'convert'))
        if not file_path:
            return Response({'error': 'Failed to download or convert video'}, status=500)

        # Save relevant data to the database
        video_download = VideoDownload.objects.create(url=url, action=action, quality=quality)

        # Create a response URL for the user to download
        download_url = reverse('download-file', kwargs={'file_name': os.path.basename(file_path)})

        return Response({'download_url': download_url}, status=200)

class DownloadFileView(View):
    def get(self, request, file_name):
        file_path = os.path.join('path/to/your/download/directory', file_name)  # Adjust to your directory
        try:
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                return response
        except FileNotFoundError:
            raise Http404("File does not exist")

def download_video(url, quality='best', convert_to_mp3=False):
    # Define a directory to store downloaded videos
    download_dir = 'path/to/your/download/directory'  # Update this to your desired download location
    os.makedirs(download_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best' if convert_to_mp3 else quality,
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_name = f"{info_dict['title']}.{info_dict['ext']}"
            return os.path.join(download_dir, file_name)  # Return the full path
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None
