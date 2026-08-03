from rest_framework.permissions import BasePermissions, SAFE_METHODS

class IsAdminOrEmployeeOrOwner(BasePermissions):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user.is_staff or user.is_employee:
            return True
        return obj.pk == user.pk

class IsAdminUser(BasePermissions):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_superuser or request.user.is_staff)
        )
    
        