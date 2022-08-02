from django.contrib import admin

from apps.music.models import Music


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    pass
