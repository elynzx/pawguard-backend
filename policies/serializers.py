from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from pets.models import Pet
from pets.serializers import CheckoutPetSerializer, PetProfileSerializer
from plans.models import Plan
from plans.serializers import PlanSerializer
from users.models import User
from users.serializers import CheckoutNewOwnerSerializer, UserProfileSerializer

from .models import Policy


class PolicySerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    pet = PetProfileSerializer(read_only=True)
    plan = PlanSerializer(read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Policy
        fields = [
            "id",
            "policy_number",
            "status",
            "status_display",
            "user",
            "pet",
            "plan",
            "start_date",
            "end_date",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "policy_number",
            "status",
            "start_date",
            "end_date",
            "created_at",
        ]


class UserNewPetPolicySerializer(serializers.Serializer):
    pet = CheckoutPetSerializer()
    plan = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.filter(is_active=True)
    )

    def validate(self, data):
        pet_data = data.get("pet")
        plan = data.get("plan")

        if pet_data and plan and pet_data.get("species") != plan.species:
            raise serializers.ValidationError(
                {"plan": "El plan seleccionado no corresponde a la especie."}
            )
        return data

    def create(self, validated_data) -> Policy:

        request_user = self.context["request"].user
        pet_data = validated_data.pop("pet")
        plan = validated_data.pop("plan")
        today = timezone.now().date()
        expiry_date = today.replace(year=today.year + 1)

        with transaction.atomic():
            new_pet = Pet.objects.create(owner=request_user, **pet_data)

            policy = Policy.objects.create(
                user=request_user,
                pet=new_pet,
                plan=plan,
                start_date=today,
                end_date=expiry_date,
                status=Policy.Status.ACTIVE,
            )
            return policy


class CheckoutPolicySerializer(serializers.Serializer):
    owner = CheckoutNewOwnerSerializer()
    pet = CheckoutPetSerializer()
    plan = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.filter(is_active=True)
    )

    def validate(self, data):
        pet_data = data.get("pet")
        plan_data = data.get("plan")

        if pet_data and plan_data and pet_data.get("species") != plan_data.species:
            raise serializers.ValidationError(
                {"plan": "El plan seleccionado no corresponde a la especie."}
            )
        return data

    def create(self, validated_data) -> Policy:
        owner_data = validated_data.pop("owner")
        pet_data = validated_data.pop("pet")
        plan = validated_data.pop("plan")
        today = timezone.now().date()
        expiry_date = today.replace(year=today.year + 1)

        with transaction.atomic():
            new_user = User.objects.create_user(
                password=None,
                is_active=False,
                **owner_data,
            )

            new_pet = Pet.objects.create(owner=new_user, **pet_data)

            policy = Policy.objects.create(
                user=new_user,
                pet=new_pet,
                plan=plan,
                start_date=today,
                end_date=expiry_date,
                status=Policy.Status.ACTIVE,
            )
            return policy
