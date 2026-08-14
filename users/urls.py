from django.urls import path

from .views import (
    AccountActivationView,
    ChangePasswordView,
    DashboardView,
    UserProfileView,
)

urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("dashboard/", DashboardView.as_view(), name="user-dashboard"),
    path("activate/", AccountActivationView.as_view(), name="account-activation"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
]
