from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, BooleanField

from api.models import Category, Order, OrderItem, Product, ShippingAddress, User


class ShippingAddressSerializer(ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = "__all__"


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    category = CategorySerializer()
    is_available = BooleanField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "stock",
            "is_featured",
            "category",
            "is_available",
            "image",
        ]


class OrderSerializer(ModelSerializer):
    shipping_address = ShippingAddressSerializer()

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'status',
            'products',
            'shipping_address',
            'order_date',
            'transaction_id',
        ]


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class UserSerializer(ModelSerializer):
    password = serializers.CharField(
        max_length=100, min_length=6, write_only=True
    )

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'password'
        ]

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(  # type:ignore
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password'),
        )
        return user
