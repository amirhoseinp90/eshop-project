"""
Views for user API endpoints.
"""
# from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.authtoken.views import ObtainAuthToken

from project.apps.users.api.base.permissions import UnauthenticatedOnlyPermission
from project.apps.users.api.v1.serializers import CreateUserSerializer, CreateTokenSerializer


class CreateUserView(CreateAPIView):
    """Create a new user in the system."""
    serializer_class = CreateUserSerializer
    permission_classes = [UnauthenticatedOnlyPermission]


class CreatTokenView(ObtainAuthToken):
    """Create token for the user."""
    serializer_class = CreateTokenSerializer
