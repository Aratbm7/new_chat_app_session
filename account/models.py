from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.sessions.base_session import AbstractBaseSession
# from django.contrib.sessions.models import Session
from uuid import uuid4
from django.db.models import Q

class GeneralDate(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True) 
    REQUIRED_FIELDS = ['email']
    def __str__(self) -> str:
        return self.username

class CustomSession(AbstractBaseSession ,GeneralDate):
    ip = models.CharField(max_length=20)
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    

        
class Profile(GeneralDate):
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    balance = models.IntegerField(default=0)
    user_code = models.CharField(max_length=128, default=uuid4)
    
    
    # def get_user_sites(self, ):
    #     Site.objects.filter(Q(profile=self) | Q(group=) )
    #     return 
    
    
    def __str__(self) -> str:
        return self.user.username
    

class Site(GeneralDate):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')

    
    support_user = models.ManyToManyField(User,
                                          related_name='suport_users',
                                          null=True)
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=255)
    uniqe_code = models.CharField(max_length=128, default=uuid4)
    group = models.ForeignKey('CustomGroup', on_delete=models.SET_NULL, null=True)
    
    def __str__(self) -> str:
        return self.name


class CustomGroup(GeneralDate):
    group_admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_groups')
    users = models.ManyToManyField(User, related_name="custom_groups")
    name = models.CharField(max_length=100)
    
    class Meta:
        unique_together = ('group_admin', 'name',)
    
# # todo:add settings
# class SiteSetting(GeneralDate):
#     site = models.ForeignKey(Site, on_delete=models.CASCADE)



# class Category(GeneralDate):
#     name = models.CharField(max_length=100)
#     users = models.ManyToManyField(User)
#     groups = models.ManyToManyField(Group)
#     site = models.ForeignKey(Site, on_delete=models.CASCADE)


# class DefaultMessage(GeneralDate):
#     site = models.ForeignKey(Site, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     question = models.TextField()
#     answer = models.TextField()


# class Star(GeneralDate):
#     score = models.IntegerField()
#     user = models.ForeignKey(User, on_delete=models.PROTECT)


# class Notification(GeneralDate):
#     text = models.TextField
#     date_start = models.DateTimeField()
#     date_end = models.DateTimeField()
#     remove = models.IntegerField(default=0)
#     view = models.IntegerField(default=0)
#     user = models.ForeignKey(User, on_delete=models.PROTECT)


# class BlockedSession(GeneralDate):
#     session = models.ForeignKey(CustomSession, on_delete=models.CASCADE)
#     date_end = models.DateTimeField(null=True)
#     ip = models.CharField()


# class AdminWorkFlow(GeneralDate):
#     #  todo:define action type
#     action = models.IntegerField(default=0)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL)
#     changes = models.TextField()
#     ip = models.CharField()


# class Plan(GeneralDate):
#     name = models.CharField
#     price = models.IntegerField
#     details = models.TextField


# class Payment(GeneralDate):
#     amount = models.IntegerField
#     status = models.IntegerField
#     txid = models.CharField


# class LoginLog(GeneralDate):
#     user_id = models.IntegerField
#     user = models.ForeignKey(User, on_delete=models.SET_NULL)
#     user_name = models.CharField()
#     lat = models.CharField()
#     lan = models.CharField()
#     location = models.CharField()
#     ip = models.CharField()
#     isp = models.CharField()