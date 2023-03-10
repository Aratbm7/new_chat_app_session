from django.db import models
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import User as InitUser
from django.contrib.sessions.base_session import AbstractBaseSession
# from django.contrib.sessions.models import Session
from django.contrib.auth.models import AbstractUser
import random
from uuid import uuid4


class User(AbstractUser):
    domain_name = models.CharField(max_length=255) 
    
    REQUIRED_FIELDS = ('email', 'domain_name', )

class CustomSession(AbstractBaseSession):
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return str(self.created_at)

        
def unique_code_generator(length=10):
    source = uuid4().hex
    result = ""
    for _ in range(length):
        result += source[random.randint(0, length)]
        print(result)

    return result


class GroupChat(models.Model):
    creator = models.CharField(max_length=32, unique=True, db_index=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    unique_code = models.CharField(
        max_length=10)
    domain_name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)


# class Member(models.Model):
#     chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     anon_user = models.ForeignKey(CustomSession, on_delete=models.CASCADE, null=True)
#     date_created = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username


class Message(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    author_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    anon_author = models.ForeignKey(CustomSession, on_delete=models.CASCADE, null=True)
    text = models.TextField(default="")
    created_at = models.DateField(auto_now_add=True)
    
    
# ----------------------------------------------------------------------------------------------------

class GeneralDate(models.Model):
    date_update = models.DateTimeField(auto_now=True)
    date_cerated = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class NotAbstract(models.Model):
    class Meta:
        abstract = False


class ChatRoom(GeneralDate, NotAbstract):
    name = models.CharField(max_length=255)
    comment = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    anon_user = models.ForeignKey(CustomSession, on_delete=models.SET_NULL, null=True)
    site = models.ForeignKey("account.Site", on_delete=models.SET_NULL, null=True)
    last_message_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(default=0)
    remove = models.IntegerField(default=0)
    ticket = models.IntegerField(default=0)
    unique_code = models.CharField(
        max_length=10, default=unique_code_generator)


# class Message(GeneralDate, NotAbstract):
#     chat_room = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL)
#     body = models.TextField()
#     user = models.ForeignKey("User")
#     session = models.ForeignKey("CustomSession")
#     status = models.IntegerField()
#     view = models.IntegerField()
#     reply = models.ForeignKey("Message", on_delete=models.CASCADE)
#     remove = models.IntegerField(default=0)


# class Attachment(GeneralDate, NotAbstract):
#     file = models.FileField()
#     file_type = models.IntegerField()
#     admin_user = models.ForeignKey(User, on_delete=models.SET_NULL)
#     support_user = models.ForeignKey(User, on_delete=models.SET_NULL)
#     message = models.ForeignKey(Message, on_delete=models.SET_NULL)
#     chat_room = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL)
#     url = models.URLField()


# class ChangeUserHistory(GeneralDate, NotAbstract):

# class Message(GeneralDate, NotAbstract):
#     chat_room = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL)
#     body = models.TextField()
#     user = models.ForeignKey("User")
#     session = models.ForeignKey("CustomSession")
#     status = models.IntegerField()
#     view = models.IntegerField()
#     reply = models.ForeignKey("Message", on_delete=models.CASCADE)
#     remove = models.IntegerField(default=0)


# class Attachment(GeneralDate, NotAbstract):

# class Message(GeneralDate, NotAbstract):
#     chat_room = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL)
#     body = models.TextField()
#     user = models.ForeignKey("User")
#     session = models.ForeignKey("CustomSession")
#     status = models.IntegerField()
#     view = models.IntegerField()
#     reply = models.ForeignKey("Message", on_delete=models.CASCADE)
#     remove = models.IntegerField(default=0)


# class Attachment(GeneralDate, NotAbstract):
#     file = models.FileField()
#     file_type = models.IntegerField()
#     admin_user = models.ForeignKey(User, on_delete=models.SET_NULL)
#     support_user = models.ForeignKey(User, on_delete=models.SET_NULL)
#     message = models.ForeignKey(Message, on_delete=models.SET_NULL)
#     chat_room = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL)
#     url = models.URLField()


# class ChangeUserHistory(GeneralDate, NotAbstract):
#     from_user = models.ForeignKey(User)
#     to_user = models.ForeignKey(User)
#     chat_room = models.ForeignKey(ChatRoom)
#     admin_user = models.ForeignKey(User, on_delete=models.SET_NULL)
#     support_user = models.ForeignKey(User, on_delete=models.SET_NULL)
#     message = models.ForeignKey(Message, on_delete=models.SET_NULL)
#     chat_room = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL)
#     url = models.URLField()


# class ChangeUserHistory(GeneralDate, NotAbstract):
#     from_user = models.ForeignKey(User)
#     to_user = models.ForeignKey(User)
#     chat_room = models.ForeignKey(ChatRoom)