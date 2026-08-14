from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from policies.models import Policy

from .models import Pet
from .serializers import (
    PetPhotoUpdateSerializer,
    PetProfileSerializer,
)


@extend_schema(tags=["Pets Dashboard Management"])
@extend_schema_view(
    list=extend_schema(
        summary="Listar las mascotas del propietario logueado",
        description="Recupera la lista exclusiva de animales protegidos vinculados a la cuenta del usuario en sesión.",
    ),
    retrieve=extend_schema(
        summary="Obtener la ficha clínica de una mascota",
        description="Muestra los atributos, especie, raza y edad declarada en meses de un animal por su UUID.",
    ),
    update=extend_schema(
        summary="Reemplazar ficha de la mascota",
        description="Modificación completa de los atributos permitidos de la mascota.",
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente datos de la mascota",
        description="Permite modificar campos cosméticos permitidos del animal sin alterar variables críticas de riesgo.",
    ),
)
class PetViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "update_photo":
            return PetPhotoUpdateSerializer
        return PetProfileSerializer

    @extend_schema(
        summary="Eliminar una mascota del sistema (Soft-Delete seguro)",
        description="Aplica una baja lógica al registro de la mascota. El sistema bloquea la eliminación si el animal cuenta con una póliza de seguros vigente activa.",
    )
    def destroy(self, request, *args, **kwargs):
        pet = self.get_object()
        has_active_policy = Policy.objects.filter(
            pet=pet,
            status=Policy.Status.ACTIVE,
        ).exists()

        if has_active_policy:
            return Response(
                {"detail": "No se puede eliminar una mascota con seguro activo"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Sincronizar la URL de la imagen emitida por Cloudinary",
        description="Recibe el string seguro de la URL generado por el cargador directo del Frontend en Cloudinary y lo asocia al avatar del animal.",
        request=PetPhotoUpdateSerializer,
        responses={200: PetPhotoUpdateSerializer},
    )
    @action(detail=True, methods=["patch"], url_path="update-photo")
    def update_photo(self, request, pk=None):

        pet = self.get_object()

        serializer = PetPhotoUpdateSerializer(
            pet,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Foto actualizada correctamente.",
                "photo_url": pet.photo_url,
            },
            status=status.HTTP_200_OK,
        )
