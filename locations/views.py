from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Clinic, District
from .serializers import ClinicSerializer, DistrictSerializer


@extend_schema(tags=["Locations"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar distritos de Lima Metropolitana",
        description="Obtiene el catálogo completo de distritos para los selectores.",
    )
)
class DistrictViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = DistrictSerializer
    queryset = District.objects.all()


@extend_schema(tags=["Locations"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar red de clínicas de la veterinaria",
        description="Recupera todas las sedes veterinarias, incluyendo coordenadas de latitud y longitud para renderizar en un mapa interactivo.",
    ),
    retrieve=extend_schema(
        summary="Obtener informacion de una clinica veterinaria",
        description="Muestra la información específica de telefono y dirección de una sede.",
    ),
)
class ClinicViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ClinicSerializer
    queryset = Clinic.objects.all()
