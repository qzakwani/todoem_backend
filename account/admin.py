from django.contrib import admin

from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(admin.ModelAdmin):    
    date_hierarchy = 'date_joined'
    empty_value_display = '--empty--'
    exclude = ('groups', 'user_permissions')
    
    list_filter = ('is_email_verified', 'private')
    readonly_fields = ('id', 'date_joined')
    list_display = ('username', 'id', 'name', 'email', 'is_email_verified', 'private')

    search_fields = ['id', 'username', 'email', 'name', 'phone_number']
    
    def get_form(self, request, obj=None, change=False, **kwargs):
        if obj is None:
            kwargs['form'] = UserCreationForm
        else:
            kwargs['form'] = UserChangeForm
        return super().get_form(request, obj, change, **kwargs)

admin.site.register(User, UserAdmin)