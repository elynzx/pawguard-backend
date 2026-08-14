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


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class DashboardView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

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


class AccountActivationView(APIView):
    permission_classes = [AllowAny]

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


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

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
