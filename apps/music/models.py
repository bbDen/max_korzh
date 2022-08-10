from django.db import models


class Music(models.Model):
    """ модель для музыки """
    title = models.CharField(max_length=255, unique=True)
    track = models.TextField()

    class Meta:
        verbose_name_plural = 'Музыка'
        verbose_name = 'Музыка'

    def __str__(self):
        return self.title


class Video(models.Model):
    """модель для фонового видео"""
    video = models.FileField()

    class Meta:
        verbose_name_plural = 'Видео'
        verbose_name = 'Видео'
