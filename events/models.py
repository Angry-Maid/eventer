from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('ON', 'Online'),
        ('OF', 'Offline'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=2, choices=EVENT_TYPE_CHOICES)
    capacity = models.IntegerField()
    event_start = models.DateTimeField()
    event_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def shortname(self):
        return f'{self.name}({self.type})'

    def __str__(self):
        return f'{self.name}({self.type}) - {self.created_at.isoformat()}'


class Attendance(models.Model):
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, related_name='attendees')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    @property
    def username(self):
        return self.user.get_username()

    def __str__(self):
        return f'{self.event.shortname()} <-> {self.user}'
