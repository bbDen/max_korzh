from django.http import HttpResponse, FileResponse
from django.utils.encoding import smart_str
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.music.models import Music, Video
from apps.music.serializers import MusicSerializer, VideoSerializer


class MusicListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = MusicSerializer
    queryset = Music.objects.all()


class VideoAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = VideoSerializer
    queryset = Video.objects.all()
