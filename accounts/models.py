from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Extend Django's built‑in user with a developer flag.

    The ``is_developer`` flag determines whether the user has
    developer privileges and can access the developer dashboard.
    Additional custom fields can be added here in the future.
    """
    is_developer = models.BooleanField(default=False)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.username
