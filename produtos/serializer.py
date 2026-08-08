from rest_framework import serializers
from models import Category, Product
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
        read_only_fields = ["id"]

    def validate_name(self, value):
        query = Category.objects.filter(name__iexact = value)

        if self.instance:
            query = query.exclude(pk = self.instance.pk)

        if query.exists():
            raise ValidationError("Category already exists. ")
        
        return value
    
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only = True)
    category_id = serializers.PrimaryKeyRelatedField(
        query_set = Category.objects.all(),
        source = "category",
        write_only = True
    )
    
    class Meta: 
        model = Product
        fields = ["id", "name", "price", "stock", "category", "category_id"]
        read_only = ["id"]


    def validate_price(self, value):
        if value <= 0:
            raise ValidationError("Price must be greater than zero.")
        return value
    
    def validate_name(self, value):
        query = Product.objects.filter(name_iexact = value)

        if self.istance:
            query = query.exclude(pk = self.instance.pk)

        if self.exists():
            raise ValidationError("A product with this name already exists. ")
        
        return value
