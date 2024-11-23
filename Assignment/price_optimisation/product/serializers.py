from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

    def validate_name(self, value):
        """
        Ensure the category name is unique (case-insensitive).
        """
        if Category.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("A category with this name already exists.")
        return value

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_name', 'cost_price', 'selling_price',
                  'description', 'stock', 'units_sold']
    
    def validate(self, data):
        # Ensure selling_price is not less than cost_price
        if data.get('selling_price') < data.get('cost_price'):
            raise serializers.ValidationError("Selling price cannot be less than cost price.")
        return data
