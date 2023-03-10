from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.base_session import AbstractBaseSession

class GeneralDate(models.Model):
    date_update = models.DateTimeField(auto_now=True)
    date_cerated = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True



class CustomSession(AbstractBaseSession ,GeneralDate):
    ip = models.CharField()
    name = models.CharField()
    email = models.EmailField()


class Profile(GeneralDate):
    parent = models.ForeignKey("self", on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    balance = models.IntegerField()
    domain_name = models.CharField(max_length=255)
    domain_owner = models.BooleanField(default=False)
    


class Site(GeneralDate):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    url = models.URLField()


# todo:add settings
class SiteSetting(GeneralDate):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)


class Group(GeneralDate):
    users = models.ManyToManyField(User, related_name="groups")
    name = models.CharField(max_length=100)


class Category(GeneralDate):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User)
    groups = models.ManyToManyField(Group)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)


class DefaultMessage(GeneralDate):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()


class Star(GeneralDate):
    score = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class Notification(GeneralDate):
    text = models.TextField
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    remove = models.IntegerField(default=0)
    view = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT)


class BlockedSession(GeneralDate):
    session = models.ForeignKey(CustomSession, on_delete=models.CASCADE)
    date_end = models.DateTimeField(null=True)
    ip = models.CharField()


class AdminWorkFlow(GeneralDate):
    #  todo:define action type
    action = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    changes = models.TextField()
    ip = models.CharField()


class Plan(GeneralDate):
    name = models.CharField
    price = models.IntegerField
    details = models.TextField


class Payment(GeneralDate):
    amount = models.IntegerField
    status = models.IntegerField
    txid = models.CharField


class LoginLog(GeneralDate):
    user_id = models.IntegerField
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    user_name = models.CharField()
    lat = models.CharField()
    lan = models.CharField()
    location = models.CharField()
    ip = models.CharField()
    isp = models.CharField()