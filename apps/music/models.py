from django.db import models


class Music(models.Model):
    title = models.CharField(max_length=255, unique=True)
    link = models.TextField()