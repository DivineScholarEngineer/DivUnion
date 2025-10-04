"""
Views for the store app.

Provide pages for browsing products, filtering by name and category and
viewing individual product details.
"""
from django.db import OperationalError
from django.shortcuts import get_object_or_404, render

from .filters import ProductFilter
from .models import Product


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
    return render(request, "store/shop.html", {
        "filter": product_filter,
        "products": products,
    })


def product_detail(request, slug: str):
    """Display details for a single product."""
    product = get_object_or_404(Product, slug=slug)
    return render(request, "store/product_detail.html", {"product": product})
