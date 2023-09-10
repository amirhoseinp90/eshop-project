"""
Models Managers
"""
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, username, email, password=None, **extra_fields):
        """Create, save and return a user with hashed password."""
        if not username:
            raise ValueError('User must have a username')

        if not email:
            raise ValueError('User must have an email address')

        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """Create and return a new superuser."""
        user = self.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user
