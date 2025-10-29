from django.db import models
from django.conf import settings
from django.urls import reverse


class Event(models.Model):
    EVENT_TYPES = (
        ("work", "Work Session"),
        ("meeting", "Meeting"),
        ("study", "Study Session"),
        ("deadline", "Deadline"),
    )
    title = models.CharField(max_length=200, default="Untitled Event")
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey('projects.Project', on_delete=models.SET_NULL, null=True, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='work')
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    tags = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.get_event_type_display()}: {self.title}"
        
    def get_absolute_url(self):
        return reverse('analytics:event_list')