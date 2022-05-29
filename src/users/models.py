from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRoleChoices(models.TextChoices):
    """."""

    PARTNER = "partner", "Partner"
    CUSTOMER = "customer", "Customer"
    ADMIN = "admin", "Admin"


class CustomUserManager(BaseUserManager):
    def create_user(self, username=None, password=None, **extra_fields):
        """."""

        email = self.normalize_email(username)
        user = self.model(username=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractUser):
    """."""

    username = models.EmailField(unique=True)
    role = models.CharField(choices=UserRoleChoices.choices, max_length=15)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
