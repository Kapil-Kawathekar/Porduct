from rest_framework.viewsets import ModelViewSet
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class CategoryListCreateAPIView(APIView):
    """
    Handles listing and creating categories.
    """
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(APIView):
    """
    Handles retrieving, updating, and deleting a specific category.
    """
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        if category is None:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ProductListCreateAPIView(APIView):
    """
    Handles listing and creating products.
    """
    def get(self, request):

        queryset = Product.objects.all()

        # Search by name or description
        search_query = request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | Q(description__icontains=search_query)
            )

        # Filter by category
        category_id = request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Filter by cost price range
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        if min_price:
            queryset = queryset.filter(cost_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(cost_price__lte=max_price)

        # Sort by attributes
        ordering = request.query_params.get('ordering', None)
        if ordering:
            queryset = queryset.order_by(ordering)

        # Serialize and return the filtered results
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailAPIView(APIView):
    """
    Handles retrieving, updating, and deleting a specific product.
    """

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return None

    def get(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        product = self.get_object(pk)
        if product is None:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({"message": "Product deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
