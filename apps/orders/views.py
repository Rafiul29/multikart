from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import transaction
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.exceptions import PermissionDenied

from .models import Order, OrderItem
from .serializers import OrderSerializer
from apps.products.models import Product
from  .pagination import OrderPagination
from .permission import IsAdmin,IsOwnOrder,IsVendorOrder

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination

    def get_permissions(self):
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied(detail={"error": "Authentication required."})

        # Admin can access everything
        if user.role == "admin":
            return [IsAuthenticated(), IsAdmin(),AllowAny()]

        # Customer permissions
        if user.role == "customer":
            if self.action in ['create']:
                return [IsAuthenticated()]
            if self.action in ['list','retrieve','partial_update']:
                return [IsAuthenticated(), IsOwnOrder()]

        # Vendor permissions
        if user.role == "vendor":
            if self.action in ['list', 'retrieve', 'update', 'partial_update', 'destroy']:
                return [IsAuthenticated(), IsVendorOrder()]

        raise PermissionDenied(detail={"error": "You do not have permission to access this resource."})
    
    def list(self, request):
        user = request.user

        if user.role == 'admin':
            orders = Order.objects.all()
        elif user.role == 'vendor':
            orders = Order.objects.filter(items__product__vendor__user=user).distinct()
        elif user.role == 'customer':
            orders = Order.objects.filter(customer=user)
        else:
            return Response({"error": "Unauthorized role."}, status=status.HTTP_403_FORBIDDEN)
        
        # Apply pagination
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request):
        user = request.user

        if user.role != 'customer':
            return Response({"error": "Only customers can place orders."}, status=status.HTTP_403_FORBIDDEN)

        items_data = request.data.get('items')
        if not items_data:
            return Response({"error": "No order items provided."}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(customer=user)

        for item in items_data:
            product_id = item.get('product')
            quantity = item.get('quantity', 1)

            if not product_id or quantity <= 0:
                transaction.set_rollback(True)
                return Response({"error": "Invalid product ID or quantity."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                transaction.set_rollback(True)
                return Response({"error": f"Product ID {product_id} not found."}, status=status.HTTP_404_NOT_FOUND)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_order=product.price
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    # partial_update on PATCH METHOD
    def partial_update(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
            self.check_object_permissions(request, order)
            
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if request.user.role=='customer' and request.data.get('status') !='cancle':
        
            return Response(
                {"error": "Customer can only cancle status updated"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        order.status = request.data.get('status', order.status)
        order.save()
        # Perform partial update using serializer
        serializer = OrderSerializer(order)
        return Response({"data": serializer.data, "success": "Order status updated."}, status=status.HTTP_200_OK)
 
    # delete order - DELETE Method
    def destroy(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
            self.check_object_permissions(request, order)
            order.delete()
            return Response({"success": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
