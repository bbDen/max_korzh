from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from apps.music.models import Music, Video


class MusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = ('title', 'track')



class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = '__all__'

    def get_video(self, obj):
        try:
            video = obj.video.url
        except:
            video = None
        return video