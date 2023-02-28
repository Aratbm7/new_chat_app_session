from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.sessions.base_session import AbstractBaseSession
# from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
import random
from uuid import uuid4

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
    date_created = models.DateTimeField(auto_now_add=True)


class Member(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    anon_user = models.ForeignKey(CustomSession, on_delete=models.CASCADE, null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    author_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    anon_author = models.ForeignKey(CustomSession, on_delete=models.CASCADE, null=True)
    text = models.TextField(default="")
    created_at = models.DateField(auto_now_add=True)