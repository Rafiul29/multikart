from django.db import models
from django.conf import settings
from apps.accounts.models import CustomUser

class Vendor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='vendor_profile')
    store_name = models.CharField(max_length=255)

    def __str__(self):
      return f"{self.user.username}---{self.store_name}"

class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products',blank=True,null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
       return f"{self.vendor.store_name} by product {self.name}"
    

    

