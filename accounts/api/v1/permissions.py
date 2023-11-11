from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    """a permission for checking user is owner/admin or not"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True

        return bool(request.user.id == obj.id)


class IsTokenOwnerOrAdmin(permissions.BasePermission):
    """a permission for checking user is owner/admin or not"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff:
            return True

        return bool(request.user.email == obj.email)
