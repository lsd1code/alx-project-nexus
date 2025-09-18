import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


class User(AbstractUser):
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
        Category, on_delete=models.DO_NOTHING, related_name="products"
    )
    image = CloudinaryField('image', null=True, blank=True)
    is_featured = models.BooleanField(default=False)

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


class Order(models.Model):
    class OrderStatusChoices(models.TextChoices):
        PENDING = "PENDING"
        CONFIRMED = "CONFIRMED"
        CANCELLED = "CANCELLED"

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
    transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id} - {self.status}"


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.DO_NOTHING, related_name="order_items"
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
