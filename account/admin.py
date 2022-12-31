from django.contrib import admin
from .models import User




class UserAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_joined'
    empty_value_display = '--empty--'
    exclude = ('groups', 'user_permissions')
    
    list_filter = ('is_email_verified',)
    readonly_fields = ('id', 'date_joined')
    list_display = ('username', 'id', 'name', 'email', 'is_email_verified')
    
    search_fields = ['id', 'username', 'email', 'name', 'phone_number']

admin.site.register(User, UserAdmin)