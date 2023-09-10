"""
Database models.
"""
import uuid
import os

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import AbstractUser
from django.db import models

from project.apps.users.managers import UserManager

def user_avatar_file_path(instance, filename):
    """Generate file path for new user avatar."""
    ext = os.path.splitext(filename)[1]
    filename = f'uploads/avatar/{uuid.uuid4()}{ext}'

    return filename

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True)
    avatar = models.ImageField(upload_to=user_avatar_file_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    objects = UserManager()

