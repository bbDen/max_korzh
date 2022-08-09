from django.http import HttpResponse, FileResponse
from django.utils.encoding import smart_str
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.music.models import Music
from apps.music.serializers import MusicSerializer


class MusicListAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = MusicSerializer
    queryset = Music.objects.all()

    def post(self, request):
        request_body = request.data
        srz = MusicSerializer(data=request_body)
        if srz.is_valid():
            srz.save()
            return Response(srz.data, status=status.HTTP_201_CREATED)
        else:
            return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)


class MusicFileGetAPIView(APIView):
    def get(self,request):
        music = Music.objects.order_by('?').first()

        # response = HttpResponse(mimetype='audio/mpeg')
        # response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(music.track.name)
        # response['Accept-Ranges'] = 'bytes'
        # response['X-Sendfile'] = smart_str(music.track.name)

        # response = HttpResponse()
        # response['Content-Type'] = 'application/mp3'
        # response['X-Accel-Redirect'] = '/files/' + music.track.name
        # response['Content-Disposition'] = 'attachment;filename=' + music.track.name
        response = FileResponse(music.track.open())
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(
            music.track.name
        )
        return response
