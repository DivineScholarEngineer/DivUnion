"""Core views for the DivUnion project."""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import OperationalError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from store.models import Product
from store import views as store_views

Feature = Dict[str, str]

CORE_FEATURES: List[Feature] = [
    {
        "icon": "🛍️",
        "title": "Curated Tech Catalogue",
        "description": "Browse a hand-picked selection of innovative gadgets sourced from trusted partners.",
    },
    {
        "icon": "🔍",
        "title": "Smart Search & Filters",
        "description": "Quickly locate products using responsive keyword and category filtering.",
    },
    {
        "icon": "🤖",
        "title": "AI Customer Support",
        "description": "Get instant answers from our on-site assistant that remembers your recent conversation.",
    },
    {
        "icon": "🧑\u200d💻",
        "title": "Developer Dashboard",
        "description": "Unlock internal insights with a developer role that exposes roadmap-ready stats.",
    },
    {
        "icon": "🔐",
        "title": "Account Management",
        "description": "Create an account to personalise your experience and manage your profile securely.",
    },
]

NEW_FEATURES: List[Feature] = [
    {
        "icon": "📱",
        "title": "Responsive Layout",
        "description": "Bootstrap-powered pages adapt gracefully to phones, tablets and desktops.",
    },
    {
        "icon": "⚡",
        "title": "Subtle Scroll Animations",
        "description": "IntersectionObserver-driven fade-ins keep the experience lively without hurting performance.",
    },
    {
        "icon": "🍪",
        "title": "Cookie Consent Controls",
        "description": "Visitors can opt in to cookies at any time thanks to our built-in banner.",
    },
    {
        "icon": "🌐",
        "title": "Static Export Ready",
        "description": "Deploy effortlessly with django-distill powering static builds for platforms like Netlify.",
    },
    {
        "icon": "📊",
        "title": "Operational Snapshot",
        "description": "The dashboard summarises catalogue counts to jump-start your product planning.",
    },
    {
        "icon": "🧭",
        "title": "Category-driven Navigation",
        "description": "Structure large inventories with reusable category records and friendly slugs.",
    },
    {
        "icon": "🖼️",
        "title": "Media-ready Listings",
        "description": "High-quality imagery and detailed descriptions bring every product to life.",
    },
    {
        "icon": "🔗",
        "title": "Marketplace Links",
        "description": "Attach optional outbound links such as eBay offers directly from product records.",
    },
    {
        "icon": "💬",
        "title": "Session-aware Conversations",
        "description": "Chat history persists for the duration of your visit so you never lose context.",
    },
    {
        "icon": "🛡️",
        "title": "Role-based Access",
        "description": "Fine-tune staff access with the extendable developer flag on custom user accounts.",
    },
]

Conversation = List[Tuple[str, str]]


def _get_products(limit: int | None = None) -> Iterable[Product]:
    """Return a list of products, swallowing database errors during builds."""

    try:
        queryset = Product.objects.all()
        if limit is not None:
            queryset = queryset[:limit]
        return list(queryset)
    except OperationalError:
        return []


def index(request: HttpRequest) -> HttpResponse:
    """Homepage showing featured products and platform highlights."""

    products = _get_products(limit=6)
    return render(
        request,
        "index.html",
        {
            "products": products,
            "core_features": CORE_FEATURES,
            "new_features": NEW_FEATURES,
        },
    )


def _generate_response(message: str) -> str:
    """Return a canned AI response based on simple keyword matching."""

    lowered = message.lower()
    if "shipping" in lowered:
        return "We ship worldwide. Orders are dispatched within two business days."
    if "support" in lowered or "help" in lowered:
        return "Our support team is available 24/7 via support@divunion.com."
    if "refund" in lowered or "return" in lowered:
        return "You can request a return within 30 days of delivery for a full refund."
    if "price" in lowered or "cost" in lowered:
        return "All prices shown include taxes; shipping is calculated at checkout."
    return "Thanks for your message! A specialist will follow up shortly."


def ai_agent(request: HttpRequest) -> HttpResponse:
    """Toy AI support chatbot that keeps a short conversation in session storage."""

    conversation: Conversation = request.session.get("ai_conversation", [])
    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()
        if user_message:
            conversation.append(("You", user_message))
            conversation.append(("DivUnion AI", _generate_response(user_message)))
            request.session["ai_conversation"] = conversation
            request.session.modified = True
    return render(request, "ai.html", {"conversation": conversation})


def contact(request: HttpRequest) -> HttpResponse:
    """Contact form that acknowledges receipt without sending email."""

    if request.method == "POST":
        messages.success(request, "Thanks! We'll be in touch soon.")
        return redirect("contact")
    return render(request, "contact.html")


@login_required
def dashboard_home(request: HttpRequest) -> HttpResponse:
    """Simple dashboard restricted to developer accounts."""

    if not getattr(request.user, "is_developer", False):
        raise PermissionDenied("Developer access required")
    stats = {"product_count": len(_get_products())}
    return render(request, "dashboard/home.html", {"stats": stats})


def shop_redirect(request: HttpRequest) -> HttpResponse:
    """Proxy to the store catalogue view while keeping the legacy URL name."""

    return store_views.shop(request)


def product_detail_static(request: HttpRequest, slug: str) -> HttpResponse:
    """Proxy product detail view used for top-level URLs and static export."""

    return store_views.product_detail(request, slug=slug)


def iter_distill_products() -> Iterable[Dict[str, str]]:
    """Yield mapping objects for each product when building static files."""

    try:
        for slug in Product.objects.values_list("slug", flat=True):
            yield {"slug": slug}
    except OperationalError:
        return
