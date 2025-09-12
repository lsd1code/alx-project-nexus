from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import Category, Product
from api.serializers import CategorySerializer, ProductSerializer


@api_view(["GET"])
def index(req: Request):

    return Response(serializer.data)
