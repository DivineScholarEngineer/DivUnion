"""
Views for the store app.

Provide pages for browsing products, filtering by name and category and
viewing individual product details.
"""
from django.shortcuts import render, get_object_or_404
from .models import Product
from .filters import ProductFilter


def shop(request):
    """Display the product catalogue with filtering options."""
    product_filter = ProductFilter(request.GET or None, queryset=Product.objects.all())
    products = product_filter.qs
    return render(request, "store/shop.html", {
        "filter": product_filter,
        "products": products,
    })


def product_detail(request, slug: str):
    """Display details for a single product."""
    product = get_object_or_404(Product, slug=slug)
    return render(request, "store/product_detail.html", {"product": product})
