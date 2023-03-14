from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.sessions.base_session import AbstractBaseSession
# from django.contrib.sessions.models import Session

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    
    
    def __str__(self) -> str:
        
        return self.user.username
    
    # def save(self, *args, **kwargs) -> None:
    #     if not self.parent:
    #         self.is_owner = True    
            
    #     super(Profile, self).save(*args, **kwargs)

    



class Site(GeneralDate):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=255)


# # todo:add settings
# class SiteSetting(GeneralDate):
#     site = models.ForeignKey(Site, on_delete=models.CASCADE)


# class Group(GeneralDate):
#     users = models.ManyToManyField(User, related_name="groups")
#     name = models.CharField(max_length=100)


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