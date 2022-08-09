from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from apps.music.models import Music


class MusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = ['title', 'track']

    def get_music(self, obj):
        try:
            music = obj.music.url
        except:
            music = None
        return music
