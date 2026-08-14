from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Policy
from .serializers import (
    CheckoutPolicySerializer,
    PolicySerializer,
    UserNewPetPolicySerializer,
)


@extend_schema(tags=["Policies & Checkout"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar el historial de pólizas contratadas",
        description="Retorna una lista con todos los contratos de seguros médicos y vigencias que le pertenecen estrictamente al usuario logueado.",
    ),
    retrieve=extend_schema(
        summary="Obtener el detalle de una póliza específica",
        description="Inspecciona el estado, número de póliza secuencial formateado y coberturas de un contrato anual por su ID.",
    ),
)
class PolicyViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PolicySerializer

    def get_queryset(self):
        return Policy.objects.filter(user=self.request.user)


@extend_schema(tags=["Policies & Checkout"])
class PolicyCheckoutView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Procesar la compra de una póliza de seguro medico",
        description=(
            "Endpoint centralizado. Si la petición proviene de un visitante anónimo (Home), "
            "crea la cuenta de usuario inactiva, la mascota y emite la póliza en una transacción. "
            "Si proviene de un cliente logueado, procesa únicamente la nueva mascota y su seguro."
        ),
        request=CheckoutPolicySerializer,
        responses={201: PolicySerializer},
    )
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = UserNewPetPolicySerializer(
                data=request.data,
                context={"request": request},
            )
        else:
            serializer = CheckoutPolicySerializer(
                data=request.data,
                context={"request": request},
            )

        serializer.is_valid(raise_exception=True)
        policy = serializer.save()

        read_serializer = PolicySerializer(policy)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)
