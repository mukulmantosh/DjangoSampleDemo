from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

from django.db import models
import time
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("Users must have an email address.")

        if not password:
            raise ValueError('Users must have an password')

        user = self.model(
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email,
                                password
                                )
        user.is_active = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255, default='user')
    last_name = models.CharField(max_length=255, default='user')
    jwt_secret = models.UUIDField(default=uuid.uuid4, null=True)
    email = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=False)
    is_company_admin = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = "email"

    class Meta:
        ordering = ["id"]

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        if self.is_superuser:
            return True
        else:
            return self.user_permissions.filter(codename=perm).exists()

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff

        return self.is_superuser
