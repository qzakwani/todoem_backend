from django.contrib import admin

from .models import TaskGroup, TaskGroupTask, TaskGroupMember


class TaskGroupAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    empty_value_display = '--empty--'
    
    readonly_fields = ('id', 'created_at')
    list_display = ('id', 'creator', 'creator_id', 'created_at')
    
    
    raw_id_fields = ('creator', 'members')
    
    search_fields = ['id', 'creator__username', 'creator__id', 'name', 'creator__name']


admin.site.register(TaskGroup, TaskGroupAdmin)



class TaskGroupTaskAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    empty_value_display = '--empty--'
    
    readonly_fields = ('id', 'created_at', 'last_modified')
    list_display = ('id', 'taskgroup', 'created_at')
    
    
    raw_id_fields = ('taskgroup', 'created_by', 'completed_by')
    
    search_fields = ['id', 'created_by__username', 'taskgroup__id', 'created_by__id', 'task']
    

admin.site.register(TaskGroupTask, TaskGroupTaskAdmin)


class TaskGroupMemberAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_added'
    empty_value_display = '--empty--'
    
    readonly_fields = ('id', 'date_added')
    list_display = ('taskgroup_id', 'member', 'member_id', 'is_admin', 'is_staff')
    
    list_filter = ('is_admin', 'is_staff')
    
    
    raw_id_fields = ('taskgroup', 'member')
    
    search_fields = ['member__username', 'member__id', 'taskgroup__id']
    

admin.site.register(TaskGroupMember, TaskGroupMemberAdmin)
