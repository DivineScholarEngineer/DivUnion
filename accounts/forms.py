from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users.

    Inherits from Django's built‑in ``UserCreationForm`` and specifies the
    custom user model.  This form can be extended to add additional
    fields if required.
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    """Form for updating existing users.

    Inherits from Django's built‑in ``UserChangeForm`` and specifies the
    custom user model.  This form can be extended to modify the list
    of editable fields.
    """

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ("username", "email", "is_developer")
