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
