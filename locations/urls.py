from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClinicViewSet, DistrictViewSet

router = DefaultRouter()
router.register("districts", DistrictViewSet, basename="district")
router.register("clinics", ClinicViewSet, basename="clinic")

urlpatterns = [path("", include(router.urls))]