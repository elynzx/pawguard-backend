from rest_framework import serializers

from .models import Clinic, District


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = [
            "id",
            "name",
        ]
        read_only_fields = [
            "id",
        ]


class ClinicSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source="district.name", read_only=True)

    class Meta:
        model = Clinic
        fields = [
            "id",
            "name",
            "address",
            "phone",
            "district",
            "district_name",
            "latitude",
            "longitude",
        ]
        read_only_fields = [
            "id",
        ]
