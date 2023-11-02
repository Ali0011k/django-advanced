from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    
    def has_permission(self, request, view):
        """ checking user is superuser/staff or not """
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_superuser or request.user.is_staff)
    
    
    def has_object_permission(self, request, view, obj):
        """ checking user is owner or not """
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.id == obj.id)