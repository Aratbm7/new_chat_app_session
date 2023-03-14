from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomSession
from django.db.models import F
from .  import serializers
from . import models
from rest_framework.viewsets import ModelViewSet
from .permissions import (personal_permissions, ProfilePermison
                          , SitePermission)
from rest_framework.permissions import AllowAny
# from django.contrib.sessions.middleware 

def exam(request):
    
    print('ip_from_view',request.session['ip_address'])
    return HttpResponse(request.META.get('REMOTE_ADDR'))



class ProfileViewSet(ModelViewSet):
    queryset = models.Profile.objects.select_related('user').all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [ProfilePermison, personal_permissions({'u':15, 'o':0})]

    def update(self, request, *args, **kwargs):
        
        return super().update(request, *args, **kwargs)
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
        return {'profile_pk': self.kwargs['profile_pk']}
    
    