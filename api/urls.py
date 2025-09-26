from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from api.views import (
    CategoryViewSet,
    ProductViewSet,
    FeaturedProducts,
    OrderViewSet,
    UserRegistration,
    UserProfileAPIView,
    index
)


router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="products")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"orders", OrderViewSet, basename="orders")


urlpatterns = [
    path(
        "", index, name="index"
    ),
    path(
        "featured-products/", FeaturedProducts.as_view(), name="featured_products"
    ),

    #! Authentication
    path(
        "accounts/profile/<str:pk>/", UserProfileAPIView.as_view(), name="user_profile"
    ),
    path(
        "accounts/auth/register/", UserRegistration.as_view(), name="register_user"
    ),
    path(
        "accounts/auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    #! Documentation
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui",
    ),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc",
    ),
] + router.urls
