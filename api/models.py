from __future__ import unicode_literals
from django.db import models


class Socket(models.Model):
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)
    name = models.TextField(default="", max_length=100)
    number = models.IntegerField(default=0)
    rapsPin = models.IntegerField(default=0)
    status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Socket, self).save(*args, **kwargs)