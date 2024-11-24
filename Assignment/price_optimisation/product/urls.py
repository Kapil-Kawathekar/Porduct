from django.urls import path
from .views import (
    ProductListCreateAPIView,
    ProductDetailAPIView,
    CategoryListCreateAPIView,
    CategoryDetailAPIView,
    RegisterUserAPIView,
    LoginAPIView
)

urlpatterns = [
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
