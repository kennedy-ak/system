from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_type', 'project', 'start_time', 'end_time', 'tags', 'metadata']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter event title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add a description...',
                'rows': 4
            }),
            'event_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'project': forms.Select(attrs={
                'class': 'form-select'
            }),
            'start_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'tags': forms.Textarea(attrs={
                'class': 'form-control font-monospace',
                'placeholder': '["work", "important"]',
                'rows': 3
            }),
            'metadata': forms.Textarea(attrs={
                'class': 'form-control font-monospace',
                'placeholder': '{"key": "value"}',
                'rows': 3
            }),
        }
