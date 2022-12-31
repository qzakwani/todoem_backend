from django.contrib import admin

from .models import TaskList, TaskListTask, SentTaskList, SentTaskListTask


class TaskListAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    empty_value_display = '--empty--'
    
    readonly_fields = ('id', 'created_at',)
    list_display = ('id', 'sender', 'receiver', 'tasks_num', 'created_at')
    
    list_filter = ('completed',)
    
    raw_id_fields = ('sender', 'receiver')
    
    search_fields = ['id', 'sender__username', 'sender__id', 'name', 'receiver__username', 'receiver__id']

admin.site.register(TaskList, TaskListAdmin)

class TaskListTaskAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('tasklist_id', 'id')
    
    raw_id_fields = ('tasklist',)
    
    search_fields = ['id', 'tasklist__id', 'task']

admin.site.register(TaskListTask, TaskListTaskAdmin)


class SentTaskListAdmin(TaskListAdmin):
    list_display = ('id', 'sender', 'receiver', 'tasks_num', 'delivered', 'created_at')
    
    list_filter = ('delivered',)


admin.site.register(SentTaskList, SentTaskListAdmin)


class SentTaskListTaskAdmin(TaskListTaskAdmin):
    pass

admin.site.register(SentTaskListTask, SentTaskListTaskAdmin)