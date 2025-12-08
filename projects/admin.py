from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'owner']
    search_fields = ['title', 'description', 'owner__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
