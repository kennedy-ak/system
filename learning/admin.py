from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'progress', 'created_at']
    list_filter = ['progress', 'created_at', 'owner']
    search_fields = ['title', 'description', 'owner__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
