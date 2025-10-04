from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    """Administration panel configuration for the custom user."""
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["username", "email", "is_developer", "is_staff", "is_active"]
    list_filter = ["is_developer", "is_staff", "is_active"]
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("is_developer",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("is_developer",)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
