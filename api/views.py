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
    """
    ListAPIView that returns featured Product instances.
    This view serves a read-only, paginated list of products with the is_featured flag set to True.
    It uses ProductSerializer to serialize Product objects and allows unrestricted access (AllowAny).
    Responses to GET requests are cached for 15 minutes (cache_page 60 * 15) using the "product_list"
    key_prefix to reduce database load for frequently requested data.
    Behavior and notes:
    - Inherits ListAPIView, so standard DRF pagination, filtering and ordering settings apply unless
        overridden at the view or project level.
    - Cache key_prefix should be unique enough to avoid collisions with other cached endpoints.
    - When featured status changes, ensure appropriate cache invalidation to keep results current.
    Usage:
    - Mount this view on a URL to expose a public endpoint that lists featured products via HTTP GET.
    """
    queryset = Product.objects.filter(is_featured=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    @method_decorator(cache_page(60 * 15, key_prefix="featured_product_list"))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductViewSet(ModelViewSet):
    """
    ProductViewSet is a ViewSet for managing Product objects.
    Features:
        - Provides CRUD operations for Product model.
        - Supports searching products by 'name' and 'slug' fields.
        - Caches the product list API response for 15 minutes using a key prefix 'product_list'.
        - Allows unauthenticated access for GET requests; other methods require authentication and admin privileges.
        - Supports filtering products by category via the 'category' query parameter (expects category slug).
    Methods:
        list(request, *args, **kwargs):
            Returns a paginated list of products, with caching applied.
        get_permissions():
            Dynamically sets permissions based on request method:
                - GET: Allows any user.
                - Other methods: Requires authenticated admin user.
        get_queryset():
            Optionally filters products by category if 'category' query parameter is provided.
    Attributes:
        queryset: Queryset of all Product objects.
        serializer_class: Serializer used for Product objects.
        filter_backends: List of filter backends (supports search).
        search_fields: Fields to search by ('name', 'slug').
        permission_classes: Default permissions (authenticated admin users).
    """
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
    """
    CategoryViewSet handles CRUD operations for Category objects.
    This viewset provides endpoints for listing, retrieving, creating, updating, and deleting categories.
    It uses slug-based lookup for retrieving individual categories. The permissions are set such that
    only authenticated admin users can perform write operations, while read operations (GET requests)
    are open to any user.
    Methods:
        get_permissions(self):
            Dynamically sets permissions based on the request method. Allows unrestricted access for GET requests,
            while restricting other methods to authenticated admin users.
        list(self, request, *args, **kwargs):
            Returns a list of all categories using the default ModelViewSet behavior.
        retrieve(self, request, slug=None):
            Retrieves a category by its slug and returns a serialized list of products associated with that category.
    Attributes:
        queryset: Queryset of all Category objects.
        serializer_class: Serializer used for Category objects.
        lookup_url_kwarg: URL keyword argument used for slug-based lookup.
        permission_classes: Default permission classes for the viewset.
    """
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
    """
    ViewSet for managing Order objects.
    This viewset provides endpoints for authenticated users to create, retrieve, and list their orders.
    It ensures that users can only access their own orders and handles order creation with associated products and shipping address.
    Methods
    -------
    get_queryset():
        Returns a queryset filtered to only include orders belonging to the authenticated user.
    retrieve(request, *args, **kwargs):
        Retrieves a specific order by its primary key, including the total price calculated from its order items.
    create(request, *args, **kwargs):
        Creates a new order for the authenticated user, including associated products and shipping address.
        Validates the presence of required fields ('products' and 'shipping_address') in the request data.
        Calculates the total price of the order based on the provided products and their quantities.
    Attributes
    ----------
    queryset : QuerySet
        The base queryset of all Order objects.
    serializer_class : Serializer
        The serializer class used for Order objects.
    permission_classes : list
        List of permission classes; only authenticated users can access these endpoints.
    Permissions
    -----------
    - Only authenticated users can access the endpoints.
    - Users can only view and create their own orders.
    Responses
    ---------
    - On successful creation, returns order ID, success message, and total price.
    - On retrieval, returns order details including total price.
    - On bad request (missing required fields), returns HTTP 400 Bad Request.
    """
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

        order = Order(user=user, shipping_address=shipping_address)
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
