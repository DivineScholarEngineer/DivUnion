"""
URL configuration for the accounts app.

Includes paths for login, logout, registration and profile pages.  The
login and logout views are provided by Django, while registration
and profile are custom.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
]
