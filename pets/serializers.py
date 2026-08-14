from rest_framework import serializers

from common.constants import PET_MAX_ENTRY_AGE_MONTHS, PET_MIN_AGE_MONTHS

from .models import Pet


class PetProfileSerializer(serializers.ModelSerializer):
    species_display = serializers.CharField(
        source="get_species_display", read_only=True
    )
    gender_display = serializers.CharField(source="get_gender_display", read_only=True)

    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "species",
            "species_display",
            "gender",
            "gender_display",
            "breed",
            "is_companion_animal",
            "photo_url",
            "declared_age_months",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "species",
            "is_companion_animal",
            "declared_age_months",
            "created_at",
        ]


class CheckoutPetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "species",
            "gender",
            "breed",
            "is_companion_animal",
            "declared_age_months",
        ]

    def validate_is_companion_animal(self, value):
        if not value:
            raise serializers.ValidationError("Solo se aceptan mascotas de compañía.")
        return value

    def validate(self, data):
        age_months = data.get("declared_age_months")

        if age_months is not None:
            if age_months < PET_MIN_AGE_MONTHS:
                raise serializers.ValidationError(
                    {
                        "declared_age_months": f"La mascota debe tener al menos {PET_MIN_AGE_MONTHS} meses de edad para acceder al plan."
                    }
                )
            if age_months > PET_MAX_ENTRY_AGE_MONTHS:
                raise serializers.ValidationError(
                    {
                        "declared_age_months": f"La edad máxima permitida es {PET_MAX_ENTRY_AGE_MONTHS} meses (10 años) para acceder al plan."
                    }
                )
        return data