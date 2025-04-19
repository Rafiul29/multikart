from rest_framework import serializers
from products.models import Vendor,Product
from accounts.serializers import CustomUserDetailsSerializer
from orders.serializers import OrderSerializer

# VendorSerialzer that include User details
class VendorSerializer(serializers.ModelSerializer):
  user = CustomUserDetailsSerializer()
  
  class Meta:
    model = Vendor
    fields = ['id','store_name','user'] # Select only the necessary fields

# ProductSerialzer that include Vendor details
class ProductSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'vendor'] # Select only the necessary fields

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value
    



# VendorSerializer that includes Products details
class VendorDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)  
    user = CustomUserDetailsSerializer(read_only=True)

    class Meta:
        model = Vendor
        fields = ['id', 'store_name', 'user', 'products'] # Select only the necessary fields
        