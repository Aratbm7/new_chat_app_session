from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
# from django.contrib.sessions.base_session import AbstractBaseSession
import random
from uuid import uuid4


# def unique_code_generator(length=10):
#     source = uuid4().hex
#     result = ""
#     for _ in range(length):
#         result += source[random.randint(0, length)]
#         print(result)

#     return result


class GeneralDate(models.Model):
    date_update = models.DateTimeField(auto_now=True)
    date_cerated = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class ChatRoom(GeneralDate):
    OFF = 0
    ON = 1
    
    STATUS = (
        (OFF, 'offline'),
        (ON, 'online')
    )
    
    REMOVED = 1
    UNREMOVED = 0   
    
    REMOVE_STATUS = (
        (UNREMOVED, 'unremoved'),
        (REMOVED, 'removed')    
    )
    
    # Admin user is admin of that site anon user goes there
    admin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='admin_users')
    name = models.CharField(max_length=255)
    comment = models.TextField(null=True)
    # any chats that it user field is null is shown to the suporters
    suporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, 
                             related_name='suporters')
    session = models.ForeignKey('account.CustomSession', on_delete=models.CASCADE)
    site = models.ForeignKey("account.Site", on_delete=models.SET_NULL, null=True)
    last_message_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(default=OFF, choices=STATUS)
    remove = models.IntegerField(default=UNREMOVED, choices=REMOVE_STATUS)
    ticket = models.IntegerField(default=0)
    unique_code = models.CharField(
        max_length=10, default=uuid4)
    group = models.ForeignKey("account.CustomGroup",
                              on_delete=models.SET_NULL, 
                              related_name='groups', 
                              null=True)


class Message(GeneralDate):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    body = models.TextField()
    user = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name='messages', null=True)
    session = models.ForeignKey("account.CustomSession",on_delete=models.CASCADE,related_name='messages', null=True)
    status = models.IntegerField(default=0)
    view = models.IntegerField(default=0)
    reply = models.ForeignKey("Message", on_delete=models.CASCADE,related_name='messages', null=True)
    remove = models.IntegerField(default=0)


# class Attachment(GeneralDate):
#     file = models.FileField()
#     file_type = models.IntegerField()
#     admin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
#     support_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
#     message = models.ForeignKey(Message, on_delete=models.SET_NULL)
#     chat_room = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL)
#     url = models.URLField()

# class ChangeUserHistory(GeneralDate):
#     from_user = models.ForeignKey(settings.AUTH_USER_MODEL)
#     to_user = models.ForeignKey(settings.AUTH_USER_MODEL)
#     chat_room = models.ForeignKey(ChatRoom)
#     admin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
#     support_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL)
#     message = models.ForeignKey(Message, on_delete=models.SET_NULL)
#     chat_room = models.ForeignKey(ChatRoom, on_delete=models.SET_NULL)
#     url = models.URLField()


# class ChangeUserHistory(GeneralDate):
#     from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)