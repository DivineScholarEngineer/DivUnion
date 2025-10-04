"""URL configuration for the DivUnion project."""

from __future__ import annotations

from typing import Dict, Iterator, Optional

from django.contrib import admin
from django.urls import include, path
from django_distill import distill_path

from . import views


def distill_none() -> Iterator[Optional[Dict[str, str]]]:
    """Helper that yields a single ``None`` value for static export."""

    yield None


def distill_products() -> Iterator[Dict[str, str]]:
    """Yield keyword arguments for each product detail page."""

    yield from views.iter_distill_products()


urlpatterns = [
    path("admin/", admin.site.urls),
    distill_path("", views.index, name="index", distill_func=distill_none),
    distill_path("ai/", views.ai_agent, name="ai", distill_func=distill_none),
    distill_path("contact/", views.contact, name="contact", distill_func=distill_none),
    distill_path("shop/", views.shop_redirect, name="shop", distill_func=distill_none),
    distill_path(
        "product/<slug:slug>/",
        views.product_detail_static,
        name="product_detail",
        distill_func=distill_products,
    ),
    path("dashboard/", views.dashboard_home, name="dashboard_home"),
    path("accounts/", include("accounts.urls")),
    path("store/", include(("store.urls", "store"), namespace="store")),
]
