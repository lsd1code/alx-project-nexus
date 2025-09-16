from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Category, Product
from api.serializers import CategorySerializer, ProductSerializer
from api.auth import obtain_token_for_user


@api_view(["GET"])
def index(req: Request):
    """
    View that welcomes the user and redirects them to the Swagger API documentation.

    Args:
        req (Request): The incoming HTTP request.

    Returns:
        Response: An HTTP response that redirects the user to the Swagger API docs.
    """
    return Response("")


# @api_view(['POST'])
# def register(req: Request):
#     email, password = req.data['email'], req.data['password']  # type:ignore

#     user = User(email=email, password=password)
#     user.save()

#     return Response(obtain_token_for_user(email, password))


# @api_view(['POST'])
# def login(req: Request):
#     data = req.data
#     return Response(obtain_token_for_user(data['email'], data['password']))


@api_view(["GET"])
def featured_products_listing(req: Request):
    """
    Retrieves a list of featured products.

    This view filters the Product queryset to include only products marked as featured
    (`is_featured=True`). The resulting queryset is serialized using the `ProductSerializer`
    and returned as a response.

    Args:
        req (Request): The HTTP request object.

    Returns:
        Response: A response object containing serialized data of featured products.

    Raises:
        None

    Example:
        GET /api/featured-products/
        Returns a JSON array of featured products.
    """
    products = Product.objects.filter(is_featured=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


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
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    search_fields = ['name', 'slug']

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
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def retrieve(self, request, slug=None):
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category)
        products_serializer = ProductSerializer(products, many=True)

        return Response(products_serializer.data)
