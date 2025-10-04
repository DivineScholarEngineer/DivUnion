"""
Views for the accounts app.

Handle user registration, profile display and any future account
management functionality.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm


def register(request):
    """Display and process the user registration form."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    """Display the profile page for the currently logged‑in user."""
    return render(request, "accounts/profile.html")
