from django.db import models
from django.conf import settings
from apps.products.models import Product
from apps.accounts.models import CustomUser

# Order model
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # One Customer can multiple order
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='OrderItem',related_name='orders')  # M2M relation Order <-> Product

    def __str__(self):
        return f"{self.customer.first_name} - {self.status}"

# OrderItem model (intermediate table)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)  # which order
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # which product
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def total_price(self):
        return self.quantity * self.price_at_order
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


