from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone


class WorkLog(models.Model):
    STATUS_CHOICES = (
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('blocked', 'Blocked'),
        ('on_hold', 'On Hold'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    notes = models.TextField(blank=True, help_text='Additional notes or observations')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='worklogs')
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='worklogs'
    )
    task = models.ForeignKey(
        'tasks.Task',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='worklogs'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['project']),
        ]
        verbose_name = 'Work Log'
        verbose_name_plural = 'Work Logs'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('worklogs:worklog_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        # Auto-set completed_at when status changes to completed
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status != 'completed':
            self.completed_at = None
        super().save(*args, **kwargs)
