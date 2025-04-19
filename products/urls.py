# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  VendorViewSet, ProductViewSet,VendorProfileView

router = DefaultRouter()

router.register(r'vendors', VendorViewSet, basename='vendor')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/vendor/', VendorProfileView.as_view(), name='vendor-profile'),  
]
