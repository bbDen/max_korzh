from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from apps.music.models import Music


class MusicSerializer(serializers.ModelSerializer):
    track = SerializerMethodField()
    class Meta:
        model = Music
        fields = ('title', 'track')

    def get_track(self, obj):
        try:
            track = obj.track.url
        except:
            track = None
        return track



