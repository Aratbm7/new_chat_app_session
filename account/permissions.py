from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.db.models import Q
from math import log2
from collections import defaultdict
from .models import Profile, Site

action_dict = {
    'retrieve': 1,
    'list': 2,
    'partially_update': 4,
    'update': 8,
    'create': 16,
    'destroy': 32,
    # for all 63
}


def return_view_action_lists(input_dict, client_type):
    if input_dict[client_type] == 0:
        return []
    x = int(log2(input_dict[client_type] + 1))
    return tuple(action_dict.keys())[:x]


def personal_permissions(input_dict):
    send_dict = defaultdict(lambda: 63)
    # print('defaultdict',send_dict)
    send_dict.update(input_dict)
    # print('update send_dict',send_dict)

    class CustomPermisson(permissions.BasePermission):

        def has_permission(self, request, view):
            user_permisson_list = return_view_action_lists(send_dict, 'u')
            admin_permisson_list = return_view_action_lists(send_dict, 'a')
            other_permisson_list = return_view_action_lists(send_dict, 'o')

            if request.user and request.user.is_authenticated:
                if view.action in user_permisson_list:
                    return True

            elif request.user.is_staff:
                if view.action in admin_permisson_list:
                    return True

            elif not request.user.is_authenticated:
                if view.action in other_permisson_list:
                    return True

            return False

    return CustomPermisson

class ProfilePermison(permissions.BasePermission):
    
    def has_permission(self, request, view):
                
        if view.action == 'list':
            return bool (request.user.is_staff)
        return True

    def has_object_permission(self, request, view, obj):
        
        if view.action in ('retrieve', 'update', 'partial_update',):
            profile = Profile.objects.select_related('user')\
                .get(user_id=request.user.id)
            return bool(profile == obj or request.user.is_staff)
    
        if view.action in ['destroy',]:
            return request.user.is_staff
        
        return False
    
class SitePermission(permissions.BasePermission):
        def has_permission(self, request, view):
            
            
            print('profile_pk from permission', self)
            if view.action in ['list', 'retrieve', 'create', 'destroy', 'partial_update', 'option']:
                if request.user.is_authenticated:
                    return bool(request.user.profile.id == int(view.kwargs['profile_pk']))
            
            return True



class CustomGroupPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            if not request.user.profile.parent:
                return False
            else:
                return True