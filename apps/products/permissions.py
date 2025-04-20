from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"


class IsOwnVendor(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow if admin or owner of the vendor profile
        return request.user.role == "admin" or obj.user == request.user

class IsOwnProduct(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.vendor.user == request.user
