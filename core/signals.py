from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.conf import settings
from djoser.signals import user_registered
from rest_framework.authtoken.models import Token

from chat.models import CustomSession


@receiver(post_save, sender=Session)
def create_custom_session(sender, **kwargs):

	session = kwargs['instance']

	CustomSession.objects.update_or_create(
		session=session,
		defaults= {'updated_at': timezone.now()}
	)

@receiver(user_registered)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        