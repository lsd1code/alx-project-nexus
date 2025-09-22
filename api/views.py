from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from rest_framework.filters import SearchFilter
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework import status

from api.models import Category, Product, Order, OrderItem, ShippingAddress
from api.serializers import CategorySerializer, ProductSerializer, OrderSerializer


@api_view(['POST'])
def register(req: Request):
    return Response("user registration")


@api_view(['POST'])
def login(req: Request):
    return Response("user registration")


@api_view(["GET"])
def index(req: Request):
    """
    View that welcomes the user and redirects them to the Swagger API documentation.

    Args:
        req (Request): The incoming HTTP request.

    Returns:
        Response: An HTTP response that redirects the user to the Swagger API docs.
    """
    return Response(reverse("swagger-ui"))


class FeaturedProducts(generics.ListAPIView):
    queryset = Product.objects.filter(is_featured=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    @method_decorator(cache_page(60 * 15, key_prefix="product_list"))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'slug']
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser
    ]

    # key-prefix: used as the key prefix for the cached api responses
    @method_decorator(cache_page(60 * 15, key_prefix="product_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def get_queryset(self):
        slug = self.request.query_params.get("category")  # type:ignore

        if slug:
            category = get_object_or_404(Category, slug=slug)
            self.queryset = self.queryset.filter(category=category)

        return self.queryset


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_url_kwarg = "slug"
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsAdminUser
    ]

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, slug=None):
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category)
        products_serializer = ProductSerializer(products, many=True)

        return Response(products_serializer.data)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user=user)

    @method_decorator(cache_page(60 * 15, key_prefix="order_list"))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        order_items = OrderItem.objects.filter(order=order)
        total_price = 0

        for item in order_items:
            total_price += item.subtotal

        data = super().retrieve(request, *args, **kwargs).data
        data['total_price'] = total_price  # type:ignore

        return Response(data, status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = request.data

        if not "products" in data or not "shipping_address" in data:
            return Response("Bad Request", status.HTTP_400_BAD_REQUEST)

        user = request.user
        user_products = data['products']
        user_shipping_address = data['shipping_address']

        shipping_address = ShippingAddress.objects.create(
            address=user_shipping_address['address'],
            city=user_shipping_address['city'],
            state=user_shipping_address['state'],
            zip_code=user_shipping_address['zip_code'],
        )
        order = Order(
            user=user, shipping_address=shipping_address
        )
        order.save()

        total_price = 0

        for prod in user_products:
            product = Product.objects.get(pk=prod['product_id'])
            quantity = prod['quantity']

            order_item = OrderItem.objects.create(
                product=product, order=order, quantity=quantity
            )
            total_price += order_item.subtotal
        return Response(
            {
                "order_id": order.id,
                "message": "Order Created Successfully",
                "total_price": total_price
            },
            status=status.HTTP_201_CREATED
        )
