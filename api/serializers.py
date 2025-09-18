from rest_framework.serializers import ModelSerializer

from api.models import Category, Order, OrderItem, Product, ShippingAddress


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
            "category"
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
            'transaction_id'
        ]


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
