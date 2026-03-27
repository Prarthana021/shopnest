from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class ProductSerializer(serializers.ModelSerializer):
    # Nest the full category object inside the product response
    # so the frontend gets category name without a second API call
    category = CategorySerializer(read_only=True)
    # Accept category_id when creating/updating a product
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'stock', 'image', 'category', 'category_id', 'created_at')
