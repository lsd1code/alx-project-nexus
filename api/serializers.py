from rest_framework.serializers import ModelSerializer

from api.models import Category, Order, OrderItem, Product, User


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "description", "price", "stock", "category"]
