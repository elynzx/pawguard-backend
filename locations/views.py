from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Clinic, District
from .serializers import ClinicSerializer, DistrictSerializer


@extend_schema(tags=["Locations"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar distritos asegurables",
        description="Obtiene el catálogo completo de distritos permitidos para poblar los selectores geográficos del formulario de compra.",
    )
)
class DistrictViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = DistrictSerializer
    queryset = District.objects.all()


@extend_schema(tags=["Locations"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar red de clínicas veterinarias afiliadas",
        description="Recupera todas las sedes veterinarias asociadas, incluyendo coordenadas de latitud y longitud para renderizar el mapa interactivo.",
    ),
    retrieve=extend_schema(
        summary="Obtener ficha técnica de una clínica veterinaria",
        description="Muestra la información específica de contacto, dirección y horarios de una sede al dar clic en su pin del mapa.",
    ),
)
class ClinicViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ClinicSerializer
    queryset = Clinic.objects.all()
