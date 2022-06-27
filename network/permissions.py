from rest_framework import permissions
from django.db.models import Q

class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class IsNotAuthenticated(permissions.BasePermission):
    """
    Allows access only to not authenticated users.
    """

    def has_permission(self, request, view):
        return bool(~Q(request.user) | ~Q(request.user.is_authenticated))