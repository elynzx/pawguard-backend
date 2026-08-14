from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PolicyCheckoutView, PolicyViewSet

router = DefaultRouter()
router.register("", PolicyViewSet, basename="policy")

urlpatterns = [
    path("checkout/", PolicyCheckoutView.as_view(), name="policy-checkout"),
    path("", include(router.urls)),
]
