from rest_framework import permissions


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_employee:
            return True
        return False


class IsCompanyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_company_admin:
            return True
        return False


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False


class IsSuperUserOrCompanyAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_company_admin or request.user.is_superuser:
            return True
        return False
