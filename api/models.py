import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from api.managers import CustomUserManage


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["email", "password"]

    objects = CustomUserManage()

    groups = models.ManyToManyField(
        "auth.Group",
        blank=True,
        related_name="api_user_set",
        related_query_name="user",
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their group.",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        blank=True,
        related_name="api_user_permissions",
        related_query_name="user",
        help_text="Specific permissions for this user.",
    )


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.slug}"


class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4())
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name="products"
    )
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)

    @property
    def is_available(self):
        return self.stock > 0

    def __str__(self):
        return f"{self.id} - {self.name}"


class Order(models.Model):
    class OrderStatusChoices(models.TextChoices):
        PENDING = "PENDING"
        CONFIRMED = "CONFIRMED"
        CANCELLED = "CANCELLED"

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="orders")
    order_date = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=255, choices=OrderStatusChoices, default=OrderStatusChoices.PENDING
    )
    transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id} - {self.user.id}"


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name="order_items"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order: {self.order}: {self.product.name} - {self.quantity}"


class ShippingAddress(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="shipping_address"
    )
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.order.id}: {self.address}"
