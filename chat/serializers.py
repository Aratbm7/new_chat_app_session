# from rest_framework.serializers import ModelSerializer
from .models import User
from django.conf import settings
from djoser.serializers import UserCreateSerializer as InitUserCreateSerializer

class UserCreateSerializers(InitUserCreateSerializer):
        
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            # settings.LOGIN_FIELD,
            # settings.USER_ID_FIELD,
            'user_name',
            'domain_name',
            "password",
        )
