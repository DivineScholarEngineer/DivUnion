"""
Views for the accounts app.

Handle user registration, profile display and any future account
management functionality.
"""
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm


def register(request):
    """Display and process the user registration form using SQLite storage."""

    form = CustomUserCreationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            # Explicitly wrap the save in an atomic transaction so that the
            # SQLite database update is applied safely.  This keeps the
            # account data consistent even if something fails midway.
            with transaction.atomic(using="default"):
                user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome to DivUnion!")
            return redirect("index")
        messages.error(request, "Please correct the errors below to finish creating your account.")
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    """Display the profile page for the currently logged‑in user."""
    return render(request, "accounts/profile.html")


def login_view(request):
    """Authenticate the user against the SQLite-backed account store."""

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Welcome back, {}!".format(user.get_short_name() or user.username))
            return redirect("index")
        messages.error(request, "We couldn't sign you in. Double-check your username and password.")
    return render(request, "accounts/login.html", {"form": form})
