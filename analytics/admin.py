from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'project', 'event_type', 'start_time', 'end_time', 'duration']
    list_filter = ['event_type', 'start_time', 'user', 'project']
    search_fields = ['title', 'description', 'user__username', 'project__title']
    date_hierarchy = 'start_time'
