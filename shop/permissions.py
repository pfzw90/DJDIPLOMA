from rest_framework.permissions import BasePermission
from rest_framework import permissions

class OnlyOwnerCanEdit(BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.id == obj.user.id or request.user.is_staff:
            return True


class OnlyAdminCanEdit(BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            return True
