from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # slug is a URL-friendly version of the name e.g. "mens-clothing"
    # used in frontend URLs instead of exposing the raw database ID
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,  # if category deleted, product stays but category becomes null
        null=True,
        related_name='products'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # DecimalField for money — never FloatField (floating point precision errors)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    # ImageField requires Pillow. upload_to sets the subfolder inside MEDIA_ROOT
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
