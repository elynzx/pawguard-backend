from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from policies.models import Policy

from .models import Pet
from .serializers import (
    PetPhotoUpdateSerializer,
    PetProfileSerializer,
)


class PetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "update_photo":
            return PetPhotoUpdateSerializer
        return PetProfileSerializer

    def destroy(self, request, *args, **kwargs):
        pet = self.get_object()
        has_active_policy = Policy.objects.filter(
            pet=pet,
            status=Policy.Status.ACTIVE,
        ).exists()

        if has_active_policy:
            return Response(
                {"detail": "No se puede eliminar una mascota con seguro activo"}
            )
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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