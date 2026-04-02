from django.contrib import admin
from .models import WorkLog


@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'user', 'project', 'created_at']
    list_filter = ['status', 'project', 'created_at']
    search_fields = ['title', 'description', 'notes']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'completed_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'notes')
        }),
        ('Associations', {
            'fields': ('project', 'task')
        }),
        ('Status', {
            'fields': ('status', 'completed_at')
        }),
        ('Metadata', {
            'fields': ('user', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.user = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs
