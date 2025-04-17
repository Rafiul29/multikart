from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('vendor', 'Vendor'),
        ('customer', 'Customer')
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES ,default='customer')

    def __str__(self):
      return f"{self.username}---{self.role}"