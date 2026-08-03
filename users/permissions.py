from rest_framework.permissions import BasePermissions, SAFE_METHODS

class IsAdminOrEmployeeOrOwner(BasePermissions):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_employee:    
            return True
        return obj == request.user
    
        