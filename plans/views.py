from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Plan
from .serializers import PlanSerializer


@extend_schema(tags=["Insurance Plans"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar planes comerciales vigentes",
        description="Obtiene el catálogo de coberturas de seguros médicos activos para mostrar en la web.",
    ),
    retrieve=extend_schema(
        summary="Obtener cobertura detallada de un plan",
        description="Muestra las especificaciones detalladas, deducibles, montos y límites financieros de un plan de seguro por su ID.",
    ),
)
class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = PlanSerializer
    queryset = Plan.objects.filter(is_active=True)
