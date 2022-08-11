from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.music.models import Music
from apps.music.serializers import MusicSerializer


class MusicListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = MusicSerializer
    queryset = Music.objects.all()
