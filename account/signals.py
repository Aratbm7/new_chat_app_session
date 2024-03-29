from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token   
from .models import Profile

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        print("auth token is created")
        Token.objects.create(user=instance)
        Profile.objects.create(user=instance)
        
        
        
