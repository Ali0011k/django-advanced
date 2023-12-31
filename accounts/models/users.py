from django.db import models
from django.contrib.auth.models import *


class CostumUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("user most have an email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("user most have is_superuser = True")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("user most have is_staff = True")
        if extra_fields.get("is_active") is not True:
            raise ValueError("user most have is_active = True")
        if extra_fields.get("is_verified") is not True:
            raise ValueError("user most have is_verified = True")
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CostumUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "Users"
