from django.contrib import admin

from apps.music.models import Music, Video


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    pass


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass
