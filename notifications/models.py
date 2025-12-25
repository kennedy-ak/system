from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class ReminderLog(models.Model):
    """Track sent reminders to prevent duplicates"""
    REMINDER_TYPES = (
        ('subscription', 'Subscription'),
        ('task', 'Task'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reminder_logs'
    )
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPES)

    # Generic relation to link to either Subscription or Task
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # Store the date we reminded about (for subscriptions: next_payment_date, for tasks: deadline)
    reminder_for_date = models.DateTimeField()

    # When the reminder was sent
    sent_at = models.DateTimeField(auto_now_add=True)

    # SMS details
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    success = models.BooleanField(default=False)
    response_detail = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id', 'reminder_for_date']),
            models.Index(fields=['user', 'reminder_type', 'sent_at']),
        ]
        # Prevent duplicate reminders for the same object and date
        unique_together = [['content_type', 'object_id', 'reminder_for_date']]

    def __str__(self):
        return f"{self.reminder_type} reminder for {self.user.username} on {self.reminder_for_date}"
