from django.contrib import admin

from .models import Task

class TaskAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    empty_value_display = '--empty--'
    
    readonly_fields = ('id', 'created_at')
    list_display = ('id', 'user', 'completed', 'created_at')
    
    list_filter = ('repeat',)
    
    
    raw_id_fields = ('user',)
    
    search_fields = ['id', 'user__username', 'user__id', 'task', 'user__name']


admin.site.register(Task, TaskAdmin)
