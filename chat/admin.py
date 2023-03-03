from django.contrib import admin
from .models import User

from django.contrib.sessions.models import Session


@admin.register(Session)
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
    fields = [ 'username', 'domain_name']