import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField

from api.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4
    )
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=255, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=255, verbose_name=_("Last Name"))
    phone_number = models.CharField(
        max_length=15, verbose_name=_("Phone Number"), blank=True, null=True
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='api_user_set',
        related_query_name='api_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='api_user_permissions_set',
        related_query_name='api_user_permission',
    )


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.slug}"


class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name="products", null=True, blank=True
    )
    image = CloudinaryField('image', null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    is_hot = models.BooleanField(default=False, null=True)
    sale_percentage = models.DecimalField(
        max_digits=2, decimal_places=2, null=True)

    @property
    def is_available(self):
        return self.stock > 0

    def __str__(self):
        return f"{self.id} - {self.name}"


class ShippingAddress(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.address} - {self.city}"


class Transaction(models.Model):
    transaction_id = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4
    )
    currency = models.CharField(max_length=10, default='zar')
    stripe_payment_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_email = models.EmailField()

    def __str__(self) -> str:
        return f'Transaction: {self.transaction_id} - {self.user_email}'


class OrderStatusChoices(models.TextChoices):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class Order(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="orders"
    )
    status = models.CharField(
        max_length=255, choices=OrderStatusChoices, default=OrderStatusChoices.PENDING
    )
    products = models.ManyToManyField(
        Product, through="OrderItem", related_name="orders"
    )
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.DO_NOTHING, related_name="shipping_address", null=True, blank=True
    )
    order_date = models.DateTimeField(auto_now=True)
    transaction_id = models.ForeignKey(
        Transaction, on_delete=models.DO_NOTHING, related_name="transaction_ids", null=True, blank=True
    )

    def __str__(self):
        return f"{self.id} - {self.status}"


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now=True)

    @property
    def subtotal(self):
        return self.product.price * self.quantity  # type:ignore

    def __str__(self):
        return f"Order: {self.order}: {self.product.name} - {self.quantity}"
