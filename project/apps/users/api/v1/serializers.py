"""
Users version 1 serializers.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers

from project.apps.users.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer for creating user."""

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)
