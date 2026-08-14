from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import Plan
from .serializers import PlanSerializer


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = PlanSerializer
    queryset = Plan.objects.filter(is_active=True)