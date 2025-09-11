from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import index

urlpatterns = [
    path("", index, name="index"),
    path("token/", TokenObtainPairView.as_view(), name="token_obatain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    # path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # path(
    #     "schema/swagger-ui/",
    #     SpectacularSwaggerView.as_view(url_name="schema"),
    #     name="swagger-ui",
    # ),
    # path(
    #     "schema/redoc/",
    #     SpectacularRedocView.as_view(url_name="schema"),
    #     name="redoc",
    # ),
]
