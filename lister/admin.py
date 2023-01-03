from django.contrib import admin

from .models import ConnectedLister, ConnectionRequest

class ConnectedListerAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_connected'
    empty_value_display = '--empty--'
    
    readonly_fields = ('id', 'date_connected')
    list_display = ('user', 'lister', 'date_connected')
    
    raw_id_fields = ('user', 'lister')
    
    
    search_fields = ['user__username', 'user__id']
    search_help_text = 'search only sender username and id'


admin.site.register(ConnectedLister, ConnectedListerAdmin)



class ConnectionRequestAdmin(admin.ModelAdmin):
    date_hierarchy = 'sent_at'
    empty_value_display = '--empty--'
    
    readonly_fields = ('id',)
    list_display = ('sender', 'sender_id', 'receiver', 'receiver_id', 'sent_at')
    
    raw_id_fields = ('sender', 'receiver')
    
    search_fields = ['id', 'sender__username', 'sender__id', 'sender__name', 'receiver__username', 'receiver__id', 'receiver__name' ]


admin.site.register(ConnectionRequest, ConnectionRequestAdmin)
