from rest_framework.viewsets import ModelViewSet
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer,SupplierSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated,AllowAny
from price_optimisation.permissions import IsAdmin, IsViewer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError



class RegisterUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            raise ValidationError("Username, email, and password are required.")

        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)




class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })



class CategoryListCreateAPIView(APIView):
    """
    Handles listing and creating categories.
    """
    permission_classes = [IsAuthenticated, IsViewer | IsAdmin]
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.groups.filter(name='admin').exists():
            return Response({"detail": "Not authorized"}, status=403)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(APIView):
    """
    Handles retrieving, updating, and deleting a specific category.
    """
    permission_classes = [IsAuthenticated, IsAdmin | IsViewer]
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
        if not request.user.groups.filter(name='admin').exists():
            return Response({"detail": "Not authorized"}, status=403)
        category = self.get_object(pk)
        if category is None:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.groups.filter(name='admin').exists():
            return Response({"detail": "Not authorized"}, status=403)
        category = self.get_object(pk)
        if category is None:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class ProductListCreateAPIView(APIView):
    """
    Handles listing and creating products.
    """
    permission_classes = [IsAuthenticated, IsAdmin | IsViewer]
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
        # serializer = SupplierSerializer(queryset, many=True)
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
    permission_classes = [IsAuthenticated, IsAdmin | IsViewer]

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
