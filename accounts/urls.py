"""URL configuration for the accounts app.

Includes paths for login, logout, registration and profile pages. The
login view is a custom wrapper around Django's authentication system so we
can surface additional SQLite-focused messaging, while logout uses the
built-in view. Registration and profile remain custom.
"""
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
]
