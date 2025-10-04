from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for categories."""
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "slug"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for products."""
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "category", "price"]
    list_filter = ["category"]
