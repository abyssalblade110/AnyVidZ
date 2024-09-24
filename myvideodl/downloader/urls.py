from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoDownloadViewSet

router = DefaultRouter()
router.register(r'videos', VideoDownloadViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

