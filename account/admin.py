from django.contrib import admin
from .models import User, Profile

# from django.contrib.sessions.models import Session
from .models import CustomSession


@admin.register(CustomSession)
class SessionAdmin(admin.ModelAdmin):

    readonly_fields = ('created', 'updated')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def created(self, obj):
        return obj.custom_session.created_at
    created.short_description = 'created_at'
    
    def updated(self, obj):
        return obj.custom_session.updated_at
    updated.short_description = 'updated_at'
    
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = [ 'username', 'is_staff', 'is_superuser', 'custom_groups']

    
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ('parent', 'user', 'balance')
    
