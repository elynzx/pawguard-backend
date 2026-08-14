from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Clinic, District
from .serializers import ClinicSerializer, DistrictSerializer


class DistrictViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = DistrictSerializer
    queryset = District.objects.all()


class ClinicViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ClinicSerializer
    queryset = Clinic.objects.all()
