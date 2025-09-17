from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import CategoryViewSet, ProductViewSet, FeaturedProducts


router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="products_listing")
router.register(r"categories", CategoryViewSet, basename="categories_listing")


urlpatterns = [
    # path("auth/register", register, name="register"),
    # path("auth/login", login, name="login"),
    path(
        "featured-products/", FeaturedProducts.as_view(), name="featured_products"
    ),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
] + router.urls
