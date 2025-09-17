import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from cloudinary.models import CloudinaryField

from api.managers import CustomUserManager


class User(AbstractBaseUser):
    pass


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
        max_digits=10, decimal_places=2, null=True, blank=True)
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


class Order(models.Model):
    class OrderStatusChoices(models.TextChoices):
        PENDING = "PENDING"
        CONFIRMED = "CONFIRMED"
        CANCELLED = "CANCELLED"

    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="orders", null=True)
    order_date = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=255, choices=OrderStatusChoices, default=OrderStatusChoices.PENDING
    )
    transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id}"  # type:ignore


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
        return f"{self.order.id}: {self.address}"  # type:ignore
