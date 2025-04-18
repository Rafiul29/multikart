from rest_framework import serializers
from products.models import Vendor,Product
from accounts.serializers import CustomUserDetailsSerializer


# VendorSerialzer that include User details
class VendorSerializer(serializers.ModelSerializer):
  user = CustomUserDetailsSerializer()
  
  class Meta:
    model = Vendor
    fields = ['id','store_name','user'] # Select only the necessary fields

# ProductSerialzer that include Vendor details
class ProductSerializer(serializers.ModelSerializer):
    vendor = VendorSerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'vendor'] # Select only the necessary fields


# VendorSerializer that includes Products details
class VendorDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)  

    class Meta:
        model = Vendor
        fields = ['id', 'store_name', 'user', 'products'] # Select only the necessary fields