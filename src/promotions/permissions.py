from rest_framework import permissions

from users.models import UserRoleChoices


class PermissionMixin:
    """."""

    role = None

    def has_permission(self, request, view):
        """."""

        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == self.role


class IsAdmin(permissions.BasePermission, PermissionMixin):
    """."""

    role = UserRoleChoices.ADMIN.value


class IsPartner(permissions.BasePermission, PermissionMixin):
    """."""

    role = UserRoleChoices.PARTNER.value


class IsCustomer(permissions.BasePermission, PermissionMixin):
    """."""

    role = UserRoleChoices.CUSTOMER.value
