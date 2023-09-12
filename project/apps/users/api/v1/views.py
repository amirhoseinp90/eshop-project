"""
Views for user API endpoints.
"""
# from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import CreateModelMixin

from project.apps.users.api.base.permissions import UnauthenticatedOnlyPermission
from project.apps.users.api.v1.serializers import CreateUserSerializer


class CreateUserView(CreateAPIView):
    """Create a new user in the system."""
    serializer_class = CreateUserSerializer
    permission_classes = [UnauthenticatedOnlyPermission]
