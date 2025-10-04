"""
Views for the store app.

Provide pages for browsing products, filtering by name and category and
viewing individual product details.
"""
from django.db import OperationalError
from django.db.models import Count, Max, Min
from django.shortcuts import get_object_or_404, render

from .filters import ProductFilter
from .models import Category, Product


def shop(request):
    """Display the product catalogue with filtering options."""
    try:
        queryset = Product.objects.all()
    except OperationalError:
        queryset = Product.objects.none()
    product_filter = ProductFilter(request.GET or None, queryset=queryset)
    try:
        products = product_filter.qs
    except OperationalError:
        products = Product.objects.none()

    sort_option = request.GET.get("sort", "name")
    sort_labels = {
        "name": "Name (A–Z)",
        "price_low_high": "Price: Low to High",
        "price_high_low": "Price: High to Low",
        "newest": "Newest Arrivals",
    }
    sort_map = {
        "name": "name",
        "price_low_high": "price",
        "price_high_low": "-price",
        "newest": "-id",
    }
    order_by = sort_map.get(sort_option, "name")
    if order_by:
        products = products.order_by(order_by)

    price_summary = products.aggregate(min_price=Min("price"), max_price=Max("price"))
    category_breakdown = (
        products.values("category__name")
        .annotate(total=Count("id"))
        .order_by("category__name")
    )

    featured_products = list(products[:3])

    try:
        categories = Category.objects.all()
    except OperationalError:
        categories = Category.objects.none()

    return render(
        request,
        "store/shop.html",
        {
            "filter": product_filter,
            "products": products,
            "sort_option": sort_option,
            "sort_labels": sort_labels,
            "price_summary": price_summary,
            "category_breakdown": category_breakdown,
            "featured_products": featured_products,
            "total_products": products.count(),
            "has_results": products.exists(),
            "all_categories": categories,
        },
    )


def product_detail(request, slug: str):
    """Display details for a single product."""
    product = get_object_or_404(Product, slug=slug)
    return render(request, "store/product_detail.html", {"product": product})
