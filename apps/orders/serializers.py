from rest_framework import serializers
from .models import Order, OrderItem
from apps.accounts.serializers import CustomUserDetailsSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price_at_order', 'total_price']
        read_only_fields = ['price_at_order', 'total_price', 'product_name']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    customer=CustomUserDetailsSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'customer', 'created_at', 'status', 'total_price', 'items']
        read_only_fields = ['customer', 'created_at', 'status', 'total_price', 'items']
