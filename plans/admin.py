from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "monthly_price",
        "species",
        "recommended",
        "is_active",
        "created_at",
    )

    list_filter = ("species", "recommended", "is_active")

    search_fields = ("name", "description")

    fieldsets = (
        (
            "Información Comercial Principal",
            {
                "fields": (
                    "name",
                    "monthly_price",
                    "species",
                    "recommended",
                    "is_active",
                )
            },
        ),
        (
            "Detalles de Cobertura & Beneficios",
            {
                "fields": ("description", "benefits"),
                "description": mark_safe(
                    "<strong style='color: #2c3e50;'>Formato de Beneficios (Benefits JSON):</strong> "
                    "Debes escribir una lista válida en formato JSON (por ejemplo: "
                    '<code>["Beneficio 1", "Beneficio 2", "Beneficio 3"]</code>). '
                    "El panel lo guardará directamente la base de datos."
                ),
            },
        ),
    )
