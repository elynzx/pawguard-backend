from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

api_v1_patterns = [
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("users/", include("users.urls")),
    path("plans/", include("plans.urls")),
    path("pets/", include("pets.urls")),
    path("policies/", include("policies.urls")),
    path("locations/", include("locations.urls")),
]

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema")),
    path("admin/", admin.site.urls),
    path("api/v1/", include((api_v1_patterns, "v1"))),
]
