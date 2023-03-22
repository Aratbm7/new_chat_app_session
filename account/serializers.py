from rest_framework import serializers 
from . import models
from djoser.serializers import UserCreateSerializer
from rest_framework.authtoken.models import Token

class CustomUserCreateSerializer(UserCreateSerializer):
    def create(self, validated_data):
        user = super().create(validated_data)
        requset = self.context['request']
        r = requset.GET.get('r', None)
        parent = models.Profile.objects.filter(user_code=r).first()
        models.Profile.objects.create(user=user, parent=parent)
        Token.objects.create(user=user)
        return user
    

class UserSerilizers(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'custom_groups']
    
    def get_custom_groups(sefl, obj):
        return obj.custom_groups.all()

class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    user = UserSerilizers(read_only=True)
    parent = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = models.Profile
        fields = ('id', 'parent', 'user_id', 'balance', 'user')

    # def validate_parent(self, value):
    #     profile = models.Profile.objects.select_related('user')\
    #         .get(user=self.context['request'].user)
    #     if value ==  profile:
    #         raise serializers.ValidationError('your parent cannot be yourself')
    #     return value

    def validate(self, data):
        profile = models.Profile.objects.select_related('user')\
            .get(user=self.context['request'].user)
        if data['parent'] ==  profile:
            raise serializers.ValidationError('your parent cannot be yourself')
        
        # user_id = self.context['user_id']
        
        # if models.Profile.objects.filter(user_id=user_id).exists(): 
        #     raise serializers.ValidationError('you have a profile already')
        return data

     
    # def create(self, validated_data):
    #     user_id = self.context['user_id']
    #     return models.Profile.objects.create(user_id=user_id, **validated_data)
    
    
    # def update(self, instance, validated_data):
    #     print('validate_data', validated_data)
    #     instance.balance = validated_data['balance']
    #     instance.parent = validated_data['parent']
    #     instance.save()
    #     return instance
    
class SiteSeializers(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    profile = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Site
        fields = '__all__'

    def validate_url(self, value):
        sites = models.Site.objects.select_related('profile')\
        .filter(profile_id=self.context['profile_pk'])\
            .values_list('url', flat=True)
        if value in sites:
            raise serializers.ValidationError('you have this urls in your sites list already')
        return value
        
    def create(self, validated_data):
        profile_pk = self.context['profile_pk']
        return models.Site.objects.create(profile_id=profile_pk, **validated_data)


class GroupSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.CustomGroup
        fields = ('id', 'name', 'users')
        
        
    def create(self, validated_data):
        
        
        
        
        return super().create(validated_data)