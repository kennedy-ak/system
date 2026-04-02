from django import forms
from .models import WorkLog


class WorkLogForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['title', 'description', 'notes', 'project', 'task', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Work Log Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe what you worked on',
                'rows': 4
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Additional notes or observations',
                'rows': 3
            }),
            'project': forms.Select(attrs={
                'class': 'form-select'
            }),
            'task': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Filter projects by user
            self.fields['project'].queryset = self.fields['project'].queryset.filter(owner=user)
            # Filter tasks by user
            self.fields['task'].queryset = self.fields['task'].queryset.filter(user=user)
