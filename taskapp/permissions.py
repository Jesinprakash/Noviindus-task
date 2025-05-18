# from rest_framework.permissions import BasePermission

# class IsAdmin(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == 'Admin'

# class IsSuperAdmin(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == 'SuperAdmin'

from rest_framework.permissions import BasePermission

class IsAdminOrSuperAdmin(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.role in ['Admin', 'SuperAdmin']

