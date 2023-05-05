from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
    
class IsAdminOrUnauthenticatedUser(permissions.BasePermission):
    """
    Allows access only to authenticated admin users or unauthenticated users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_staff or
            not request.user.is_authenticated
        )