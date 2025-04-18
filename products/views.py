from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated,AllowAny



from .models import Vendor
from accounts.models import CustomUser
from .serializers import VendorSerializer
from .permissions import IsAdmin, IsOwnVendor
from .pagination import VendorPagination




class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    pagination_class = VendorPagination
    permission_classes = [IsAuthenticated]  # base permission

    def get_permissions(self):
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied(detail={"error":"Authentication required."})

        # 
        if user.role == "admin":
            return [IsAuthenticated(),IsAdmin(),AllowAny()]
        
        elif user.role == "vendor":
            if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
                return [IsAuthenticated(), IsOwnVendor()]
            elif self.action == 'create':
                return [IsAuthenticated()]
            # elif self.action == 'list':
            #     return [IsAuthenticated()]  # Will filter inside list()
        
        raise PermissionDenied(detail={"error": "You do not have permission to access this resource."})

    def list(self, request, *args, **kwargs):
        print(request.user.role)

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


    def retrieve(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(pk=pk)
            self.check_object_permissions(request, vendor)
            serializer = self.get_serializer(vendor)
            return Response({"data": serializer.data, "success": "Vendor details fetched."})
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)

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

    def destroy(self, request, pk=None):
        try:
            vendor = Vendor.objects.get(pk=pk)
            self.check_object_permissions(request, vendor)
            vendor.delete()
            return Response({"success": "Vendor deleted."})
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
