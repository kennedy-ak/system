from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'project', 'status', 'priority', 'deadline', 'created_at']
    list_filter = ['status', 'priority', 'created_at', 'deadline', 'user', 'project']
    search_fields = ['title', 'description', 'user__username', 'project__title']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
