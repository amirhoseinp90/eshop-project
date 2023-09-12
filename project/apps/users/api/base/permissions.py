"""
Custom permissions.
"""
from rest_framework.permissions import BasePermission


class UnauthenticatedOnlyPermission(BasePermission):
    """Custom permission to allow only unauthenticated users."""

    def has_permission(self, request, view):
        """check if request is unathenticated."""
        return not request.user.is_authenticated
