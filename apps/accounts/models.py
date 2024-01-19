from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from utilities.common_abstract_models import BaseAbstract


class User(AbstractUser, BaseAbstract):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name="Groups",
        blank=True,
        related_name="custom_users",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="User Permissions",
        blank=True,
        related_name="custom_users",
    )
