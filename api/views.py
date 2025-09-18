from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

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
from api.serializers import CategorySerializer, ProductSerializer, OrderSerializer, OrderItemSerializer


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
    API view to retrieve a list of featured products.

    This view returns all products that are marked as featured (`is_featured=True`).
    It uses the `ProductSerializer` to serialize the product data and allows unrestricted access
    to any user (no authentication required).

    Attributes:
        queryset (QuerySet): The queryset of featured products.
        serializer_class (Serializer): The serializer used for product representation.
        permission_classes (list): List of permission classes applied to the view.

    Methods:
        get(request, *args, **kwargs): Returns a list of featured products.
    """
    queryset = Product.objects.filter(is_featured=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    @method_decorator(cache_page(60 * 15, key_prefix="product_list"))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ProductViewSet(ModelViewSet):
    """
    A viewset for viewing and editing Product instances.
    This viewset provides the following functionality:
    - Lists all products or filters products by category slug via query parameter.
    - Uses `ProductSerializer` for serialization.
    - Allows search filtering.
    - Restricts access to authenticated admin users by default, but allows unrestricted access for GET requests.
    - Overrides `get_permissions` to allow public access for GET requests.
    - Overrides `get_queryset` to support filtering products by category slug.
    Attributes:
        queryset (QuerySet): The base queryset of all Product instances.
        serializer_class (Serializer): The serializer class for Product.
        filter_backends (list): List of filter backends to use for filtering.
        permission_classes (list): List of permission classes for access control.
    Methods:
        get_permissions(self): Returns the permission classes based on the request method.
        get_queryset(self): Returns the queryset, optionally filtered by category slug.
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
    A viewset for handling Category objects and their related Products.
    This viewset provides CRUD operations for Category instances, with custom permission handling:
    - Allows any user to perform GET requests (list and retrieve).
    - Restricts other methods (POST, PUT, DELETE) to authenticated admin users.
    Attributes:
        queryset (QuerySet): All Category objects.
        serializer_class (Serializer): Serializer for Category objects.
        lookup_url_kwarg (str): URL keyword argument used to look up Category by slug.
        permission_classes (list): Default permissions (authenticated admin users).
    Methods:
        get_permissions():
            Dynamically sets permissions based on request method.
            - GET requests are allowed for any user.
            - Other methods require admin authentication.
        retrieve(request, slug=None):
            Retrieves a Category by slug and returns serialized data for all Products in that Category.
            - Args:
                request (Request): The HTTP request object.
                slug (str, optional): The slug of the Category to retrieve.
            - Returns:
                Response: Serialized data of products belonging to the specified Category.
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


# class OrderViewSet(ModelViewSet):
#     """
#     OrderViewSet handles CRUD operations for Order objects, restricted to authenticated users.
#     This viewset provides the following functionality:
#     - Lists orders belonging to the authenticated user.
#     - Allows creation of new orders with associated shipping address and order items.
#     - Ensures only authenticated users can access order endpoints.
#     Methods:
#         get_queryset(self):
#             Returns a queryset filtered to orders belonging to the current user.
#         create(self, request, *args, **kwargs):
#             Creates a new order for the authenticated user.
#             Expects 'products' (list of product_id and quantity) and 'shipping_address' (address details) in request data.
#             Validates input, creates ShippingAddress, Order, and OrderItem instances.
#             Returns order ID and success message on completion.
#     Attributes:
#         queryset: All Order objects.
#         serializer_class: Serializer for Order objects.
#         permission_classes: Restricts access to authenticated users only.
#     Raises:
#         Returns HTTP 400 Bad Request if required fields are missing in request data.
#     """
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [
#         permissions.IsAuthenticated
#     ]

#     def get_queryset(self):
#         user = self.request.user
#         return super().get_queryset().filter(user=user)

#     def create(self, request, *args, **kwargs):
#         data = request.data

#         if not "products" in data or not "shipping_address" in data:
#             return Response("Bad Request", status.HTTP_400_BAD_REQUEST)

#         user = request.user
#         user_products = data['products']
#         user_shipping_address = data['shipping_address']

#         shipping_address = ShippingAddress.objects.create(
#             address=user_shipping_address['address'],
#             city=user_shipping_address['city'],
#             state=user_shipping_address['state'],
#             zip_code=user_shipping_address['zip_code'],
#         )
#         order = Order(
#             user=user, shipping_address=shipping_address
#         )
#         order.save()

#         for p in user_products:
#             product = Product.objects.get(pk=p['product_id'])
#             quantity = p['quantity']

#             OrderItem.objects.create(
#                 product=product, order=order, quantity=quantity
#             )

#         return Response({"order_id": order.id, "message": "Order Created Successfully"})
