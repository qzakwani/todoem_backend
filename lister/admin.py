from django.contrib import admin

from .models import Lister, ConnectionRequest

class ListerAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_connected'
    empty_value_display = '--empty--'
    
    readonly_fields = ('id',)
    list_display = ('user', 'lister', 'date_connected')
    
    raw_id_fields = ('user', 'lister')
    
    search_fields = ['id', 'user__username', 'user__id', 'lister__username', 'lister__id']


admin.site.register(Lister, ListerAdmin)



class ConnectionRequestAdmin(admin.ModelAdmin):
    date_hierarchy = 'sent_at'
    empty_value_display = '--empty--'
    
    readonly_fields = ('id',)
    list_display = ('sender', 'receiver', 'sent_at')
    
    raw_id_fields = ('sender', 'receiver')
    
    search_fields = ['id', 'sender__username', 'sender__id', 'sender__name', 'receiver__username', 'receiver__id', 'receiver__name' ]


admin.site.register(ConnectionRequest, ConnectionRequestAdmin)
