import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pawguard_backend.settings")
django.setup()

from users.models import User

email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
first_name = os.environ.get("DJANGO_SUPERUSER_FIRST_NAME", "Admin")
last_name = os.environ.get("DJANGO_SUPERUSER_LAST_NAME", "PawGuard")

if email and password:
    if not User.objects.filter(email=email).exists():
        print(f"Creando superusuario administrado por email: {email}...")

        admin_data = {
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "dni": "00000000",
            "phone": "000000000",
            "address": "Admin Address",
        }

        User.objects.create_superuser(**admin_data)
        print("Superusuario creado con exito")
    else:
        print(f"El usuario con email {email} ya existe.")
else:
    print(
        "Falta configurar DJANGO_SUPERUSER_EMAIL o DJANGO_SUPERUSER_PASSWORD en Render."
    )
