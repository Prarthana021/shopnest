from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryListView(generics.ListAPIView):
    """GET /api/products/categories/ — returns all categories. Public."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductListView(generics.ListAPIView):
    """
    GET /api/products/ — returns all products. Public.
    Supports:
      ?search=shirt        — searches name and description
      ?category=1          — filters by category ID
      ?ordering=price      — sorts by price (use -price for descending)
    """
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

    def get_queryset(self):
        queryset = Product.objects.select_related('category').all()
        # filter by category if query param provided
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    """GET /api/products/<id>/ — returns single product. Public."""
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
