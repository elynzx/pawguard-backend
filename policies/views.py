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


class PolicyViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PolicySerializer

    def get_queryset(self):
        return Policy.objects.filter(user=self.request.user)


class PolicyCheckoutView(APIView):
    permission_classes = [AllowAny]

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
