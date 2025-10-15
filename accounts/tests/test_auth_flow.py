"""Tests covering the account registration and login flows."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class AuthenticationFlowTests(TestCase):
    """Verify users can register and sign in without hitting server errors."""

    def test_registration_logs_in_user(self) -> None:
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "a-strong_password123",
                "password2": "a-strong_password123",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("index"))
        self.assertTrue(User.objects.filter(username="newuser").exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_with_valid_credentials(self) -> None:
        User.objects.create_user(
            username="registered",
            email="registered@example.com",
            password="another-strong_password123",
        )

        response = self.client.post(
            reverse("login"),
            {
                "username": "registered",
                "password": "another-strong_password123",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("index"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
