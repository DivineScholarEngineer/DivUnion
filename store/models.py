from django.db import models


class Category(models.Model):
    """Product category allowing grouping of similar items."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class Product(models.Model):
    """Individual product available for purchase."""
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    ebay_url = models.URLField(blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name
