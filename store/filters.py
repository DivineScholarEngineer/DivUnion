import django_filters
from .models import Product, Category


class ProductFilter(django_filters.FilterSet):
    """Filter products by name and category for the shop search."""
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains", label="Name")
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), label="Category")

    class Meta:
        model = Product
        fields = ["name", "category"]
