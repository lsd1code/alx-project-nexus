from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManage(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier for authentication instead of usernames.
    """

    def create_user(self, email, password, **kwargs):
        """
        Create and save a user with the given credentials
        """
        if not email:
            raise ValueError(_("The Email must be set."))
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Create and save a Superuser with the given credentials
        """
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if kwargs.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_superuser(email, password, **kwargs)
