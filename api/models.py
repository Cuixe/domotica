from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from utils import logger, raspberry
from batch.workers import TaskManager


class Pin(models.Model):
    pin_number = models.IntegerField(default=0)
    output = models.BooleanField(default=False)
    type = models.IntegerField(default=0)

    class Meta:
        ordering = ('pin_number',)

    def __str__(self):
        return "Pin " + str(self.pin_number)

    def save(self, *args, **kwargs):
        raspberry.call_pin(self.pin_number, self.output)
        super(Pin, self).save(*args, **kwargs)
        logger.debug(logger_name="Models", msg=("Pin: " + str(self.pin_number) + (' Turned On' if self.output else ' Turned Off')))


class Socket(models.Model):
    owner = models.ForeignKey('auth.User', related_name='snippets')
    pin = models.ForeignKey(Pin)
    name = models.CharField(max_length=20, default="")
    socket_number = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Event(models.Model):
    pin = models.ForeignKey(Pin)
    name = models.CharField(max_length=20, default="")
    description = models.TextField(default="")
    event_output = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=20, default="")
    execution_time = models.TimeField(default=timezone.now)
    execution_days = models.CharField(max_length=20, default="")
    events = models.ManyToManyField(Event)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        logger.info(logger_name="Models", msg="Event Changed")
        tmp = super(Task, self)
        tmp.save(*args, **kwargs)
        tmp.refresh_from_db()
        TaskManager.update_task(self.id)
