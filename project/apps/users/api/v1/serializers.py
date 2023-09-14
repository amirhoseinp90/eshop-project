"""
Users version 1 serializers.
"""
from django.contrib.auth import get_user_model, authenticate

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


class CreateTokenSerializer(serializers.Serializer):
    """Serializer for creating token."""
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get(
                'request'), email=email, password=password)

            if not user:
                msg = 'email or password is wrong'
                raise serializers.ValidationError(msg)

        else:
            msg = 'email or password must be provided'
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs
