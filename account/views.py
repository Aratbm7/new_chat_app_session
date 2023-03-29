from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from .  import serializers
from . import models
from rest_framework.viewsets import ModelViewSet
from .permissions import (personal_permissions, ProfilePermison
                          , SitePermission, CustomGroupPermission)
from rest_framework.decorators import action
from djoser.views import UserViewSet

class CustomUserViewSet(UserViewSet):
    def get_serializer_context(self):
        return {'request': self.request}


def exam(request):
    
    print('ip_from_view',request.session['ip_address'])
    return HttpResponse(request.META.get('REMOTE_ADDR'))



class ProfileViewSet(ModelViewSet):
    queryset = models.Profile.objects.select_related('user').all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [ProfilePermison, personal_permissions({'u':31, 'o':0})]
    http_method_names = ['get', 'delete', ]
    
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_update(self, serializer):
        return super().perform_update(serializer)
    
    def get_serializer_context(self):
      
        return {'user_id': self.request.user.id, 'request': self.request}
      
class SiteViewSet(ModelViewSet):
    serializer_class = serializers.SiteSeializers
    permission_classes = [SitePermission, personal_permissions({'o':0, 'u':63})]
    
    
    def get_queryset(self):
        print('sefl.kwargs', self.kwargs)

        return  models.Site.objects.select_related('profile')\
            .select_related('profile__user')\
            .filter(profile=self.kwargs['profile_pk'])
    

    def get_serializer_context(self):
        return {'profile_pk': self.kwargs['profile_pk'], 
                'request': self.request}
    
class GroupViewSet(ModelViewSet):
    # queryset = 
    serializer_class = serializers.GroupSerializers
    permission_classes = [CustomGroupPermission]
    
    
    def get_serializer_context(self):
        return {'request':self.request}
    
    def perform_create(self, serializer):
        admin_user = self.request.user
        serializer
        return super().perform_create(serializer)
    
    def get_queryset(self):
        if self.request.method == 'GET':
            
            groups= self.request.user.admin_groups.all()
            print(groups)
            return groups
        return models.CustomGroup.objects.all()

    
    