from django.contrib import admin

from .models import Clinic, District


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "address",
        "phone",
        "district",
        "latitude",
        "longitude",
    )

    search_fields = ("name", "address", "phone")

    autocomplete_fields = ["district"]
