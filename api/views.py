from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Category, Product
from api.serializers import CategorySerializer, ProductSerializer


@api_view(["GET"])
def featured_products_listing(req: Request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    permission_classes = [permissions.AllowAny]
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        slug = self.request.query_params.get("category")

        if slug:
            category = get_object_or_404(Category, slug=slug)
            self.queryset = self.queryset.filter(category=category)

        return self.queryset

    # def retrieve(self, request, slug=None):
    #     product = get_object_or_404(Product, slug=slug)
    #     serializer = ProductSerializer(product)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_url_kwarg = "slug"
    # permission_classes = [permissions.IsAuhenticated, permissions.IsAdminUser]

    def retrieve(self, request, slug=None):
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category)
        products_serializer = ProductSerializer(products, many=True)

        return Response(products_serializer.data)
