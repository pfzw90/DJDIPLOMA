from rest_framework.permissions import BasePermission
from rest_framework import permissions


class ListViewPermission(BasePermission):

    def has_permission(self, request, view):
        return True


class OnlyOwnerCanEdit(ListViewPermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.id == obj.user.id or request.user.is_staff:
            return True


class OnlyOwnerCanSee(ListViewPermission):

    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.user.id or request.user.is_staff:
            return True


class OnlyAdminCanEdit(ListViewPermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_staff:
            return True
