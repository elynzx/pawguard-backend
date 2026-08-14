<p align="center">
  <img src=".github/assets/pawguard-logo.png" alt="PawGuard logo" width="110"/>
</p>

<h1 align="center">PawGuard Backend</h1>

<p align="center">
  REST API for PawGuard, a pet insurance platform for Peru.
  <br/>
  Powers user authentication, pet management, plan contracting, and policy tracking.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Django-5.x-092E20?style=flat-square&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/DRF-3.x-A30000?style=flat-square"/>
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/JWT-Auth-F5A623?style=flat-square&logo=jsonwebtokens&logoColor=white"/>
  <img src="https://img.shields.io/badge/Swagger-Docs-85EA2D?style=flat-square&logo=swagger&logoColor=black"/>
</p>

---

## What is PawGuard?

PawGuard is a **REST API** for a pet insurance web platform focused on the Peruvian market.
It allows users to browse insurance plans, contract a policy for their pet, and manage their account and coverage from a personal dashboard.

Inspired by real pet insurance products like Pacífico Pet, the platform models annual policies with monthly payments, age-based eligibility rules, and a multi-step checkout flow.

> **Project status:** Backend API completed and deployed. Frontend built with React (separate repository).


## Key features

| Feature | Description |
|---|---|
| JWT Authentication | Login with email and password using SimpleJWT |
| Account activation | Accounts created at checkout are activated via email + DNI verification |
| Pet management | Register pets with species, breed, age, and companion status |
| Insurance plans | Browse and compare plans filtered by pet species |
| Policy contracting | Full checkout flow for new and existing users |
| Annual policies | Contracts are annual with monthly payment model |
| Soft delete | Records are never permanently deleted — deleted_at timestamp approach |
| Clinic network | Affiliated vet clinics with geolocation and district filtering |
| Admin panel | Full Django admin for plan, clinic, and policy management |
| Swagger docs | Interactive API documentation at `/api/docs/` |


## Tech stack

| Layer | Technology |
|---|---|
| Framework | Django 5 + Django REST Framework |
| Database | PostgreSQL 16 |
| Auth | SimpleJWT |
| Migrations | Django ORM |
| API docs | drf-spectacular (Swagger UI) |
| Deploy | Render |



## Business rules

- Insurable species: **dogs and cats**
- Minimum age to contract: **5 months**
- Maximum age to enter: **10 years (120 months)**
- Maximum permanence age: **11 years and 364 days (143 months)**
- Policy duration: **1 year**
- Payment model: **monthly**
- Age rules are global — not stored per plan


---

## Getting started

### Prerequisites

- Python 3.11+
- PostgreSQL 16+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/elynzx/pawguard-backend.git
cd pawguard-backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root folder:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/pawguard_db
```

### 5. Set up the database

```bash
# Create the database in psql
CREATE DATABASE pawguard_db;

# Run migrations
python manage.py migrate
```

### 6. Load initial data

```bash
# Load Lima districts
python manage.py loaddata districts

# Load clinic network
python manage.py loaddata clinics

# Load insurance plans
python manage.py loaddata plans
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

| URL | Description |
|---|---|
| `http://localhost:8000/admin/` | Django admin panel |
| `http://localhost:8000/api/docs/` | Swagger UI |


---

## Project structure

```
pawguard-backend/
├── config/
│ ├── settings.py
│ └── urls.py
├── common/
│ ├── models.py # BaseModel with UUID, soft delete, timestamps
│ └── constants.py # Age eligibility rules
├── users/
│ ├── models.py # CustomUser — email login, account_activated_at
│ ├── managers.py # UserManager — email-based auth
│ ├── serializers.py
│ ├── views.py
│ └── urls.py
├── pets/
├── plans/
├── policies/
├── locations/
└── manage.py
```


## Key design decisions

**Email as login identifier** — `username` field removed. Users authenticate with email + password.

**Inactive accounts at checkout** — when a new user contracts a policy, their account is created with `is_active=False` and no password. They activate it later via email + DNI verification.

**Soft delete** — no record is permanently deleted. `deleted_at` timestamp approach across all models via `BaseModel`.

**Age rules as constants** — eligibility ages are defined in `common/constants.py` and applied in serializer validation, not stored per plan.

**Policy number** — auto-generated as `PG-{year}-{sequence}` using an `AutoField` sequence on the `Policy` model.

**Species-plan matching** — each plan is associated with a species (dog or cat). The checkout validates that the pet species matches the selected plan.


---


## API endpoints

Base URL: `https://pawguard-backend-9t0w.onrender.com/api/v1/`

All private routes require::
```
Authorization: Bearer <your_jwt_token>
```

### Auth

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/login/` | Login and receive JWT token pair |
| `POST` | `/api/v1/auth/token/refresh/` | Refresh access token |

### Authentication — Account activation

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/users/activate/` | Activate account with email + DNI |

### User Profile Dashboard

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/users/dashboard/` | User profile + active pets + active policies |
| `GET` | `/api/v1/users/profile/` | Get authenticated user profile |
| `PATCH` | `/api/v1/users/profile/` | Update phone, address, or district |
| `POST` | `/api/v1/users/change-password/` | Change password |

### Insurance Plans

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/plans/` | List active insurance plans |
| `GET` | `/api/v1/plans/{id}/` | Get detailed plan coverage |

### Pets Dashboard

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/pets/` | List authenticated owner's pets |
| `GET` | `/api/v1/pets/{id}/` | Get pet profile |
| `PATCH` | `/api/v1/pets/{id}/` | Partially update pet data |
| `DELETE` | `/api/v1/pets/{id}/` | Soft delete pet |
| `PATCH` | `/api/v1/pets/{id}/update-photo/` | Sync Cloudinary photo URL |

### Policies & Checkout

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/policies` | List contracted policies |
| `GET` | `/api/v1/policies/{id}/` | Get policy detail |
| `POST` | `/api/v1/policies/checkout/` | Contract a new insurance policy |

### Locations

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/locations/districts/` | List Lima Metropolitana districts |
| `GET` | `/api/v1/locations/clinics/` | List affiliated vet clinics |
| `GET` | `/api/v1/locations/clinics/{id}/` | Get clinic detail |
| `GET` | `/api/v1/locations/clinics/?district={id}` | Filter clinics by district |

---

## Documentation

| URL | Description |
|---|---|
| `/api/schema/` | OpenAPI schema (JSON) |
| `/api/docs/swagger/` | Swagger UI |
| `/api/docs/redoc/` | ReDoc UI |
| `/admin/` | Django admin panel |

Live docs: `https://pawguard-backend-9t0w.onrender.com/api/docs/swagger/`

---

## Deployment

Deployed on **Render**.

| | |
|---|---|
| **Live API** | `https://pawguard-backend-9t0w.onrender.com/api/v1/` |
| **Swagger UI** | `https://pawguard-backend-9t0w.onrender.com/api/docs/swagger/` |
| **ReDoc** | `https://pawguard-backend-9t0w.onrender.com/api/docs/redoc/` |
| **Admin** | `https://pawguard-backend-9t0w.onrender.com/admin/` |


## License

Developed as an academic project for a full-stack bootcamp.
Open for educational use.


<p align="center">Build with ♡ by <a href="https://github.com/elynzx">@elynzx</a> · <a href="https://linkedin.com/in/evelynpascualc">LinkedIn</a></p>