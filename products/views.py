from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.exceptions import ValidationError

from .models import Vendor, Product
from accounts.models import CustomUser
from .serializers import VendorSerializer,ProductSerializer
from .permissions import IsAdmin, IsOwnVendor, IsOwnProduct
from .pagination import VendorPagination



# Vendor view Set
class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    pagination_class = VendorPagination
   
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
    pagination_class = VendorPagination

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]  # Anyone can view products
        if not self.request.user.is_authenticated:
            raise PermissionDenied({"error": "Authentication required."})

        user = self.request.user

        if user.role == "admin":
            return [IsAuthenticated(), IsAdmin(),AllowAny()]
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



