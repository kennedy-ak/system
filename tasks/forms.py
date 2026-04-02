from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'status', 'priority', 'deadline', 'reminder_minutes_before', 'enable_reminders']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Task description (optional)'}),
            'project': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'reminder_minutes_before': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 5}),
            'enable_reminders': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_reminder_minutes_before(self):
        minutes = self.cleaned_data.get('reminder_minutes_before')
        if minutes is not None and minutes < 0:
            raise ValidationError("Reminder time must be positive.")
        if minutes is not None and minutes > 10080:  # 1 week in minutes
            raise ValidationError("Reminder time cannot exceed 1 week (10080 minutes).")
        return minutes

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now():
            raise ValidationError("Deadline cannot be in the past.")
        return deadline
