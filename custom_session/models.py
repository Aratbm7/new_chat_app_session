from django.db import models
from django.contrib.sessions.models import Session

class CustomSession(Session):
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)

