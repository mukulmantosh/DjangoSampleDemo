from rest_framework import permissions


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_employee:
            return True


class IsCompanyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_company_admin:
            return True


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True


class IsSuperUserOrCompanyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_company_admin or request.user.is_superuser:
            return True
