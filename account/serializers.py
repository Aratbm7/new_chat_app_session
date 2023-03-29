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

    def validate(self, data):
        profile = models.Profile.objects.select_related('user')\
            .get(user=self.context['request'].user)
        if data['parent'] ==  profile:
            raise serializers.ValidationError('your parent cannot be yourself')

        return data

  
class SiteSeializers(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = models.Site
        fields =('id', 'name', 'url', 'groups', 'support_users', 'user')
        
    def get_fields(self):
        fields = super().get_fields()
        user = self.context['request'].user
        groups = models.CustomGroup.objects\
            .select_related('group_admin')\
                .prefetch_related('users')\
                    .filter(group_admin=user)
        fields['groups'] = serializers.PrimaryKeyRelatedField(many=True, queryset=groups)
        users = models.User.objects\
            .select_related('profile')\
                .filter(profile__parent__user=user)
        fields['support_users'] = serializers.PrimaryKeyRelatedField(many=True, queryset=users)
        return fields
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['support_users'] = [support_user.username for support_user in instance.support_users.all()]
        representation['groups'] = [group.name for group in instance.groups.all()]
        return representation
    
    def validate_url(self, value):
        site = models.Site.objects.select_related('user')\
        .filter(user=self.context['request'].user, url=value).first()
        request = self.context['request']
        if request.method == 'POST' and site:
            raise serializers.ValidationError('you have this urls in your sites list already')
        return value
        
   
    def create(self, validated_data):
        user = self.context['request'].user
        groups_data = validated_data.pop('groups', [])
        support_users_data = validated_data.pop('support_users', [])
        a= models.Site.objects.create(**validated_data, user=user, )
        a.groups.add(*groups_data)
        a.support_users.add(*support_users_data)
        return a



    
class GroupSerializers(serializers.ModelSerializer):
    group_admin = serializers.StringRelatedField(read_only=True)
    # users = serializers.SerializerMethodField()

    
    class Meta:
        model = models.CustomGroup
        fields = ('id', 'name', 'users','group_admin' )
        
    def get_fields(self):
        fields = super().get_fields()
        user = self.context['request'].user
        users = models.User.objects.filter(profile__parent__user=user)
        fields['users'] = serializers.PrimaryKeyRelatedField(many=True, queryset=users)
        return fields

    # def get_users(self, obj):
    #     users = obj.users.all()
    #     username = [user.username for user in users]
    #     return username
        
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['users'] = [user.username for user in instance.users.all()]
        return representation
    
    def validate(self, data):
        request = self.context['request']
        if (request.method == 'POST' and 
            request.user.admin_groups.filter(name=data['name']).first()):
                raise serializers.ValidationError('you already have group with this name')
            
        return data
        
        
    def create(self, validated_data):
        user = self.context['request'].user
        users = validated_data.pop("users")
        a = models.CustomGroup.objects.create(**validated_data, group_admin = user)
        a.users.add(*users)
        return a


