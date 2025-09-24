from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def validate_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Please provide a valid email address"))

    def create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError(_("Please provide an email address"))

        email = self.normalize_email(email)
        self.validate_email(email)

        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_verified', True)

        if kwargs.get("is_staff") is not True:
            raise ValueError(_("is_staff must be set to True for admin user"))

        if kwargs.get("is_superuser") is not True:
            raise ValueError(
                _("is_superuser must be set to True for admin user"))

        if kwargs.get("is_verified") is not True:
            raise ValueError(
                _("is_verified must be set to True for admin user"))

        user = self.create_user(
            email, password, **kwargs
        )
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=255, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last Name"))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email
