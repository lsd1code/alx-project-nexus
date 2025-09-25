from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.conf import settings
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

from api.models import Category, Product, Order, OrderItem, ShippingAddress, User, OrderStatusChoices
from api.serializers import CategorySerializer, ProductSerializer, OrderSerializer, UserSerializer, TransactionSerializer
from api.auth import get_tokens_for_user
from api.permissions import CustomerProfileAccessPermission

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


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


class UserProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    UserProfileAPIView is a Django REST Framework view that provides 
    retrieve, update, and destroy operations for user profile instances.

    This view is based on the RetrieveUpdateDestroyAPIView class, which 
    allows for the following HTTP methods:
    - GET: Retrieve a user profile by its ID.
    - PUT: Update an existing user profile.
    - PATCH: Partially update an existing user profile.
    - DELETE: Remove a user profile from the database.

    Attributes:
        queryset (QuerySet): A QuerySet containing all User objects.
        serializer_class (Serializer): The serializer class used to 
        validate and serialize the user profile data.
        permission_classes (list): A list of permission classes that 
        determine access to this view. In this case, it requires the 
        user to be authenticated and checks for custom permissions 
        defined in CustomerProfileAccessPermission.

    Usage:
        This view can be used in conjunction with a URL routing 
        configuration to allow clients to interact with user profiles 
        via a RESTful API.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        CustomerProfileAccessPermission
    ]


class UserRegistration(generics.CreateAPIView):
    """
    API view for user registration.
    This view handles the creation of new user accounts via POST requests.
    It uses the `UserSerializer` to validate and save user data. Upon successful
    registration, it generates JWT tokens for the newly created user and returns
    a response containing a welcome message, the tokens, and the serialized user data.
    Methods:
        create(request, *args, **kwargs):
            Handles POST requests for user registration.
            - Validates incoming data.
            - Saves the new user if data is valid.
            - Generates JWT tokens for the user.
            - Returns a response with a welcome message, tokens, and user data.
    Returns:
        Response: 
            - 201 Created with user data and tokens on success.
            - 400 Bad Request if the input data is missing or invalid.
    Raises:
        ValidationError: If the provided data fails serializer validation.
    Attributes:
        serializer_class (UserSerializer): The serializer class used for validating and saving user data.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data

        if not data:
            return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        tokens = get_tokens_for_user(
            user=User.objects.get(pk=serializer.data['id'])
        )

        return Response({
            "message": f"Hi {data['first_name']}, thanks for signing up!",
            "jwt_tokens": tokens,
            "data": serializer.data,
        })


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
        permissions.AllowAny
    ]

    # key-prefix: used as the key prefix for the cached api responses
    @method_decorator(cache_page(60 * 15, key_prefix="product_list"))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_permissions(self):
        if self.request.method != 'GET':
            self.permission_classes = [
                permissions.IsAdminUser,
                permissions.IsAuthenticated
            ]
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

        if len(data['products']) < 1:
            return Response("Bad Request", status.HTTP_400_BAD_REQUEST)

        user = request.user

        try:
            user_products = data['products']
            user_shipping_address = data['shipping_address']

            shipping_address = ShippingAddress.objects.create(
                address=user_shipping_address['address'],
                city=user_shipping_address['city'],
                state=user_shipping_address['state'],
                zip_code=user_shipping_address['zip_code'],
            )
        except Exception:
            return Response({"message": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order(user=user, shipping_address=shipping_address)
        order.save()

        total_amount = 0

        for prod in user_products:
            product = Product.objects.get(pk=prod['product_id'])
            quantity = prod['quantity']

            order_item = OrderItem.objects.create(
                product=product, order=order, quantity=quantity)

            total_amount += order_item.subtotal

        try:
            currency = 'usd'

            intent = stripe.PaymentIntent.create(
                amount=int(total_amount),
                currency=currency
            )

            transaction_data = {
                'amount': total_amount,
                'currency': currency,
                'stripe_payment_id': intent['client_secret'],
                'user_email': user.email
            }

            serializer = TransactionSerializer(data=transaction_data)

            if serializer.is_valid():
                model_instance = serializer.save()

                order.transaction_id = model_instance  # type:ignore
                order.status = OrderStatusChoices.CONFIRMED
                order.save()

                return Response({
                    "order_id": order.id,
                    "message": "Order Created Successfully",
                    "total_amount": total_amount,
                    'client_secret': intent['client_secret'],
                    'transaction': serializer.data
                }, status=status.HTTP_201_CREATED)

        except stripe.error.StripeError as e:  # type:ignore
            order.status = OrderStatusChoices.CANCELLED

            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
