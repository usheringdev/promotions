from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

from users.models import UserRoleChoices


class PermissionMixin:
    """."""

    curr_user_role = None

    def has_permission(self, request, view):
        """."""

        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(request.user, AnonymousUser):
            return False
        return request.user.role == self.curr_user_role


class IsAdmin(PermissionMixin, permissions.BasePermission):
    """."""

    curr_user_role = UserRoleChoices.ADMIN


class IsPartner(PermissionMixin, permissions.BasePermission):
    """."""

    curr_user_role = UserRoleChoices.PARTNER


class IsCustomer(PermissionMixin, permissions.BasePermission):
    """."""

    curr_user_role = UserRoleChoices.CUSTOMER
