"""
URL configuration for the store app.

Includes paths for viewing the product catalogue and individual product
detail pages.
"""
from django.urls import path
from . import views


urlpatterns = [
    path("", views.shop, name="shop"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
]
