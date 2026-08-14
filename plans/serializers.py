from rest_framework import serializers

from .models import Plan


class PlanSerializer(serializers.ModelSerializer):
    species_display = serializers.CharField(
        source="get_species_display", read_only=True
    )

    class Meta:
        model = Plan
        fields = [
            "id",
            "name",
            "species",
            "species_display",
            "monthly_price",
            "description",
            "recommended",
            "benefits",
            "is_active",
        ]