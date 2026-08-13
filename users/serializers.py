from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as ExceptionError
from django.utils import timezone
from rest_framework import serializers

from locations.models import District
from users.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source="district.name", read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "dni",
            "phone",
            "address",
            "district",
            "district_name",
        ]
        read_only_fields = ["email", "dni"]


class CheckoutNewOwnerSerializer(serializers.Serializer):
    email = serializers.EmailField()
    dni = serializers.CharField(max_length=8)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    phone = serializers.CharField(max_length=9)
    address = serializers.CharField(max_length=300)
    district = serializers.PrimaryKeyRelatedField(queryset=District.objects.all())

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ya existe una cuenta con este correo.")
        return value

    def validate_dni(self, value):
        if not value.isdigit() or len(value) != 8:
            raise serializers.ValidationError("El DNI debe tener 8 dígitos numéricos.")
        if User.objects.filter(dni=value).exists():
            raise serializers.ValidationError("Ya existe una cuenta con este DNI.")
        return value

    def validate_phone(self, value):
        if not value.isdigit() or len(value) != 9:
            raise serializers.ValidationError(
                "El teléfono debe tener 9 dígitos numéricos."
            )
        return value

    def create(self, validated_data) -> User:
        user = User.objects.create_user(
            password=None,
            is_active=False,
            **validated_data,
        )
        return user


class ActivateAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    dni = serializers.CharField(max_length=8)
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    def validate_dni(self, value):
        if not value.isdigit() or len(value) != 8:
            raise serializers.ValidationError("El DNI debe tener 8 dígitos numéricos.")
        return value

    def validate(self, data):
        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError(
                {"password": "Las contraseñas no coinciden."}
            )

        try:
            validate_password(data["password"])
        except ExceptionError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        try:
            user = User.objects.get(email=data["email"], dni=data["dni"])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "Los datos proporcionados no coinciden con ninguna cuenta."}
            )

        if user.account_activated_at is not None:
            raise serializers.ValidationError(
                {"email": "Esta cuenta ya fue activada anteriormente."}
            )

        self.context["user_to_activate"] = user
        self.context["clean_password"] = data["password"]
        return data

    def save(self) -> User:
        user = self.context["user_to_activate"]
        password = self.context["clean_password"]

        user.set_password(password)
        user.account_activated_at = timezone.now()
        user.is_active = True

        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context["request"].user

        if not user.check_password(data["current_password"]):
            raise serializers.ValidationError(
                {"current_password": "La contraseña actual es incorrecta."}
            )
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Las contraseñas no coinciden."}
            )
        try:
            validate_password(data["new_password"])
        except ExceptionError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        self.context["new_clean_password"] = data["new_password"]
        return data

    def save(self) -> User:
        user = self.context["request"].user
        password = self.context["new_clean_password"]

        user.set_password(password)
        user.save()
        return user
