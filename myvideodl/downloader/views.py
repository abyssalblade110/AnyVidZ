from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import VideoDownload
from .serializers import VideoDownloadSerializer
import yt_dlp
import os
from moviepy.editor import VideoFileClip
from django.utils import timezone
import time
from django.http import FileResponse

class VideoDownloadViewSet(viewsets.ModelViewSet):
    queryset = VideoDownload.objects.all()  # Keep this to satisfy ModelViewSet
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

        # Response without file_path, as requested
        response_data = {
            'url': url,
            'action': action,
            'quality': quality,
            'file_path': None,
            'timestamp': timezone.now().isoformat()  # Add current timestamp
        }

        return Response(response_data, status=200)

    @action(detail=False, methods=['post'])
    def bulk_download(self, request):
        # Placeholder for bulk download functionality
        return Response({'error': 'Bulk download not implemented'}, status=501)


def download_video(url, quality='best', convert_to_mp3=False):
    output_folder = os.path.join(os.path.expanduser('~'), 'Downloads')  # Ensure this path exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ydl_opts = {
        'format': 'bestaudio/best' if convert_to_mp3 else quality,
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),  # Ensure correct file naming
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_name = f"{info_dict['title']}.{info_dict['ext']}"
            file_path = os.path.join(output_folder, file_name)

            print(f"Downloaded file path: {file_path}")  # Ensure this shows the correct path

            if convert_to_mp3 and file_path.endswith('.mp4'):
                mp3_file_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}.mp3")
                convert_to_mp3_format(file_path, mp3_file_path)
                return mp3_file_path

            return file_path
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None



def convert_to_mp3_format(mp4_file_path, mp3_file_path):
    try:
        video = VideoFileClip(mp4_file_path)
        audio = video.audio
        audio.write_audiofile(mp3_file_path)
        audio.close()
        video.close()
        os.remove(mp4_file_path)
    except Exception as e:
        print(f"Error converting to MP3: {e}")
        return None


# Inside your view if you want to return a file to the user
def serve_file_response(file_path):
    file_name = os.path.basename(file_path)
    try:
        file_response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_name)
        file_response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return file_response
    except Exception as e:
        print(f"Error serving file: {e}")
        return None
