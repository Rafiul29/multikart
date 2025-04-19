from rest_framework import permissions
from .models import Order

class IsOwnOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer == request.user

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "admin"

class IsVendorOrder(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj.items.all())
        vendor_products = [item.product.vendor.user for item in obj.items.all()]
        print(request.user in vendor_products)
        return request.user in vendor_products
