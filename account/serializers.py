from rest_framework import serializers 
from . import models

class UserSerilizers(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',]

class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    user = UserSerilizers(read_only=True)
    
    class Meta:
        model = models.Profile
        fields = ('id', 'parent', 'user_id', 'balance', 'user')

    def validate_parent(self, value):
        profile = models.Profile.objects.select_related('user')\
            .get(user=self.context['request'].user)
        if value ==  profile:
            raise serializers.ValidationError('your parent cannot be yourself')
        return value

    # def validate(self, data):
    #     profile = models.Profile.objects.get(user=self.context['request'].user)
    #     print(data)
    #     print(type(data['parent']))
    #     if data['parent'] ==  profile:
    #         raise serializers.ValidationError('your parent cannot be yourself')
    #     return data

     
    def create(self, validated_data):
        user_id = self.context['user_id']
        return models.Profile.objects.create(user_id=user_id, **validated_data)
    
    
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

        
    def create(self, validated_data):
        profile_pk = self.context['profile_pk']
        return models.Site.objects.create(profile_id=profile_pk, **validated_data)
