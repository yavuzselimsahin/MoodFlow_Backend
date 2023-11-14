import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from rest_framework_simplejwt.tokens import OutstandingToken, BlacklistedToken

class CustomUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set')
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set')
    bio = models.CharField(max_length=255, blank=True)
    display_name = models.CharField(max_length=255, blank=True)
    cover_photo = models.ImageField(upload_to='covers/', null=True, blank=True)


