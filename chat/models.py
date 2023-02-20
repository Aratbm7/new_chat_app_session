from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.sessions.base_session import AbstractBaseSession
# from django.contrib.sessions.models import Session
# from django.contrib.auth.models import User
# import random
# from uuid import uuid4

# from django.utils import timezone



class CustomSession(AbstractBaseSession):
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    # def save(self, *args, **kwargs):
    #     if not self.session_key:
    #         created_at =  timezone.now()
            
    #     return super(CustomSession, self).save(*args, **kwargs)


        
# def unique_code_generator(length=10):
#     source = uuid4().hex
#     result = ""
#     for _ in range(length):
#         result += source[random.randint(0, length)]
#         print(result)

#     return result


# class GroupChat(models.Model):
#     creator = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=255, blank=False, null=False)
#     unique_code = models.CharField(
#         max_length=10, default=unique_code_generator)
#     date_created = models.DateTimeField(auto_now_add=True)


# class Member(models.Model):
#     chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     date_created = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username


# class Message(models.Model):
#     chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     text = models.TextField(default="")
#     created_at = models.DateField(auto_now_add=True)