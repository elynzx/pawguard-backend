from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pets.models import Pet
from pets.serializers import PetProfileSerializer
from policies.models import Policy
from policies.serializers import PolicySerializer

from .serializers import (
    ActivateAccountSerializer,
    ChangePasswordSerializer,
    UserProfileSerializer,
)


@extend_schema(tags=["User Profile Dashboard"])
@extend_schema_view(
    retrieve=extend_schema(
        summary="Obtener datos del perfil del propietario",
        description="Consulta la información personal del usuario logueado. Protegido internamente contra ataques IDOR de URL.",
    ),
    update=extend_schema(
        summary="Reemplazar datos del perfil",
        description="Modificación total de los campos permitidos de contacto del propietario.",
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente el perfil",
        description="Permite modificar campos específicos como teléfono o dirección sin alterar datos estáticos como DNI o Correo.",
    ),
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


@extend_schema(tags=["User Profile Dashboard"])
class DashboardView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Obtener el panel de datos consolidado",
        description="Endpoint agregador avanzado de rendimiento. Devuelve el perfil del dueño, sus mascotas y sus pólizas vigentes.",
    )
    def get(self, request, *args, **kwargs):
        active_user = request.user

        user_pets = Pet.objects.filter(owner=active_user)

        user_policies = Policy.objects.filter(
            user=active_user, status=Policy.Status.ACTIVE
        )

        return Response(
            {
                "user": UserProfileSerializer(active_user).data,
                "pets": PetProfileSerializer(user_pets, many=True).data,
                "policies": PolicySerializer(user_policies, many=True).data,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["Authentication"])
class AccountActivationView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Activar una cuenta de usuario pre-creada",
        description="Flujo público post-checkout. Valida la correspondencia cruzada de DNI + Correo, establece la contraseña comercial y activa la cuenta.",
        request=ActivateAccountSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = ActivateAccountSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Cuenta activada correctamente"},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["User Profile Dashboard"])
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Cambiar la contraseña desde el Dashboard",
        description="Valida la contraseña actual del usuario y establece de forma segura la nueva contraseña hasheada en la base de datos.",
        request=ChangePasswordSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Contraseña actualizada correctamente."},
            status=status.HTTP_200_OK,
        )
