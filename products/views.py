from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.exceptions import ValidationError

from .models import Vendor, Product
from accounts.models import CustomUser
from .serializers import VendorSerializer,ProductSerializer
from .permissions import IsAdmin, IsOwnVendor, IsOwnProduct
from .pagination import VendorPagination,ProductPagination



# Vendor view Set
class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    pagination_class = VendorPagination
   
    #  set up a custom permission
    def get_permissions(self):
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied(detail={"error":"Authentication required."})
        if  self.action == 'create':
            return [IsAuthenticated()]
        if user.role == "admin":
            return [IsAuthenticated(),IsAdmin(), AllowAny()]
        
        elif user.role == "vendor":
            if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
                return [IsAuthenticated(), IsOwnVendor()]
            # elif self.action == 'create':
            #     print("dwffwfwefwefwef")
            #     return [IsAuthenticated()]
            # elif self.action == 'list':
            #     return [IsAuthenticated()]  # Will filter inside list()
        
        raise PermissionDenied(detail={"error": "You do not have permission to access this resource."})

    # Retrive all vendor list - GET Method
    def list(self, request, *args, **kwargs):

        if request.user.role == "admin":
            queryset = Vendor.objects.all()
        elif request.user.role == "vendor":
            queryset = Vendor.objects.filter(user=request.user)
        else:
            return Response({"error": "You do not have permission to view vendors."},
                            status=status.HTTP_403_FORBIDDEN)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "data": serializer.data,
            "success": "Fetched vendors successfully."
        })

    #  Retrive single Vendor - Get Method /id
    def retrieve(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(pk=pk)
            self.check_object_permissions(request, vendor)
            serializer = self.get_serializer(vendor)
            return Response({"data": serializer.data, "success": "Vendor details fetched."})
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)

    #  Create a new vendor - POST method
    def create(self, request, *args, **kwargs):
        user = None
        store_name = request.data.get('store_name')
        # if vendor create admin provided to the user_id and store_name other wise provided to the only store name
        if request.user.role=='admin':
            user_id = request.data.get('user_id')
            user = CustomUser.objects.get(id=user_id);
        else:
            user = request.user

        if not store_name:
            return Response({"error": "Store name is required"}, status=status.HTTP_400_BAD_REQUEST)

        if Vendor.objects.filter(user=user).exists():
            return Response({"error": "You already have a vendor profile"}, status=status.HTTP_400_BAD_REQUEST)

        vendor = Vendor.objects.create(user=user, store_name=store_name)

        # update user role
        user.role='vendor'
        user.save()

        serializer = VendorSerializer(vendor)
        return Response({"data": serializer.data, "success": "Vendor profile created."}, status=status.HTTP_201_CREATED)

    # Update hole document - PUT Mehtod
    def update(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(pk=pk)
            self.check_object_permissions(request, vendor)

            store_name = request.data.get('store_name')
            if not store_name:
                return Response({"error": "Store name is required"}, status=status.HTTP_400_BAD_REQUEST)

            vendor.store_name = store_name
            vendor.save()
            serializer = VendorSerializer(vendor)
            return Response({"data": serializer.data, "success": "Vendor updated."})
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

    # Update selected Field for -  PATCH Method
    def partial_update(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(pk=pk)
            self.check_object_permissions(request, vendor)

            vendor.store_name = request.data.get('store_name', vendor.store_name)
            vendor.save()
            serializer = VendorSerializer(vendor)
            return Response({"data": serializer.data, "success": "Vendor partially updated."})
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

    #  Delete a single vendor - DELETE Method
    def destroy(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(pk=pk)
            # update user role
            user = vendor.user
            user.role = 'customer'
            user.save()

            self.check_object_permissions(request, vendor)
            vendor.delete()
           
            return Response({"success": "Vendor deleted."})
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)


# Modify Custom error response
def flatten_errors(error_dict):
    flat_errors = {}
    for field, errors in error_dict.items():
        if isinstance(errors, dict):
            # Handle nested error dicts
            for subfield, suberrors in errors.items():
                if isinstance(suberrors, list) and suberrors:
                    flat_errors[field] = suberrors[0]
        elif isinstance(errors, list) and errors:
            flat_errors[field] = errors[0]
        else:
            flat_errors[field] = str(errors)
    return flat_errors

# Product view Set
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    #set up a custom permission
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]  # Anyone can view products
        if not self.request.user.is_authenticated:
            raise PermissionDenied({"error": "Authentication required."})

        user = self.request.user

        # if user role is admin can perform all method post,get,delete update
        if user.role == "admin":
            return [IsAuthenticated(), IsAdmin(),AllowAny()]
        # if user  role is vendor can perform method post,get delete, update his own product
        elif user.role == "vendor":
            if self.action in ['create','update', 'partial_update', 'destroy']:
                return [IsAuthenticated(), IsOwnProduct()]
            return [IsAuthenticated()]
        
        raise PermissionDenied({"error": "You do not have permission to access this resource."})

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Product.objects.all()

        if user.role == "admin":
            return Product.objects.all()
        elif user.role == "vendor":
            return Product.objects.filter(vendor__user=user)
        elif user.role == "customer":
            return Product.objects.all()
        return Product.objects.none()
    
    # create new Product
    def create(self, request, *args, **kwargs):
        user = request.user

        # If the user is a vendor, assign the product to their vendor profile
        if user.role == "vendor":
            try:
                vendor = Vendor.objects.get(user=user)
            except Vendor.DoesNotExist:
                return Response({"error": "Vendor profile not found."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You do not have permission to create a product."}, status=status.HTTP_403_FORBIDDEN)

        # Validate other fields using the serializer
        serializer = ProductSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            flat_errors = flatten_errors(e.detail)
            return Response({"error": flat_errors}, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        # Now manually create the product, associating it with the vendor
        product = Product.objects.create(
            vendor=vendor,  # Vendor is already set from the authenticated user
            name=validated_data['name'],
            description=validated_data['description'],
            price=validated_data['price'],
            stock=validated_data['stock']
        )

        response_serializer = ProductSerializer(product)
        return Response({"data": response_serializer.data, "success": "Product created."}, status=status.HTTP_201_CREATED)

    # #  retrive single Product Get(id)
    # def retrieve(self, request, pk=None):
    #     try:
    #         user = self.request.user
    #         # First, check if the user is authenticated
    #         if user.is_authenticated:
    #             # Then, check if the user is a vendor
    #             if user.role == "vendor":
    #                 product = Product.objects.get(pk=pk, vendor__user=user)
    #                 print(product, 'Product for vendor')
    #             else:
    #                 # Handle case where the user is authenticated but not a vendor
    #                 return Response({"error": "You are not authorized to view this product."}, status=status.HTTP_403_FORBIDDEN)
    #         else:
    #             # If the user is not authenticated
    #             return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

    #         print(product, user.role)
    #         self.check_object_permissions(request, product)
    #         serializer = self.get_serializer(product)
    #         return Response({"data": serializer.data, "success": "product details fetched."})
    #     except Product.DoesNotExist:
    #         return Response({"error": "Product not found or not owned by you."}, status=status.HTTP_404_NOT_FOUND)

    # Update product hole document
    def update(self, request, pk=None):
        user = request.user

        # Allow only vendors or admins
        if user.role not in ["vendor", "admin"]:
            return Response({"error": "You do not have permission to update a product."}, status=status.HTTP_403_FORBIDDEN)

        try:
            if user.role == "admin":
                product = Product.objects.get(pk=pk)  # Admins can access any product
            elif user.role == "vendor":
                product = Product.objects.get(pk=pk, vendor__user=user)  # Vendors can access only their own products
        except Product.DoesNotExist:
            return Response({"error": "Product not found or not owned by you."}, status=status.HTTP_404_NOT_FOUND)


        # Validate input
        serializer = ProductSerializer(product, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            flat_errors = flatten_errors(e.detail)
            return Response({"error": flat_errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({"data": serializer.data, "success": "Product updated."}, status=status.HTTP_200_OK)
    
    # update product selected field - Patch Method
    def partial_update(self, request, pk=None):
        user = request.user

        # Allow only vendors or admins
        if user.role not in ["vendor", "admin"]:
            return Response({"error": "You do not have permission to update a product."}, status=status.HTTP_403_FORBIDDEN)

        try:
            if user.role == "admin":
                product = Product.objects.get(pk=pk)  # Admins can access any product
            elif user.role == "vendor":
                product = Product.objects.get(pk=pk, vendor__user=user)  # Vendors can access only their own products
        except Product.DoesNotExist:
            return Response({"error": "Product not found or not owned by you."}, status=status.HTTP_404_NOT_FOUND)

        # Apply partial updates
        product.name = request.data.get('name', product.name)
        product.description = request.data.get('description', product.description)
        product.price = request.data.get('price', product.price)
        product.stock = request.data.get('stock', product.stock)

        # Validation
        if product.price <= 0:
            return Response({"error": "Price must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)
        if product.stock < 0:
            return Response({"error": "Stock cannot be negative."}, status=status.HTTP_400_BAD_REQUEST)

        product.save()
        serializer = ProductSerializer(product)
        return Response({"data": serializer.data, "success": "Product partially updated."}, status=status.HTTP_200_OK)

    #  Delete a single Product - DELETE Method
    def destroy(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
            self.check_object_permissions(request, product)
            product.delete()
           
            return Response({"success": "Product deleted."})
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)








