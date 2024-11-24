from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        # Allow access if the user is in the "admin" group
        return request.user.groups.filter(name='admin').exists()

class IsViewer(BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access for "viewer" group
        if request.user.groups.filter(name='viewer').exists():
            return request.method in ['GET', 'HEAD', 'OPTIONS']
        return False

class IsSupplier(BasePermission):
    def has_permission(self, request, view):
        # Allow read-only access for "viewer" group
        if request.user.groups.filter(name='supplier').exists():
            return request.method in ['GET', 'HEAD', 'OPTIONS']
        return False