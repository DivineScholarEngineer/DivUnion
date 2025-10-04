"""URL configuration for the store app."""

from __future__ import annotations

from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("", views.shop, name="shop"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
]
