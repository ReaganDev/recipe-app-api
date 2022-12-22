from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin,)

# Create your models here.


class UserManager(BaseUserManager):
    """Manager for users"""

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """create, save and return a new user"""
        if not email:
            raise ValueError("The given email must be set")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # if extra_fields.get("is_staff") is not True:
        #     raise ValueError("Superuser must have is_staff=True.")
        # if extra_fields.get("is_superuser") is not True:
        #     raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """user in the system"""
    # id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
