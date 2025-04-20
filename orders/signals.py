from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Order, OrderItem

@receiver(post_save, sender=OrderItem)
def notify_vendor_on_orderitem_created(sender, instance, created, **kwargs):
    print('calling',instance)
    if created:
        vendor = instance.product.vendor
        email = vendor.user.email

        if email:
            send_mail(
                subject='📦 New Order Received!',
                message=f'Dear {vendor.store_name},\n\nYou have a new order containing your product(s).',
                from_email='no-reply@snapmart.com',
                recipient_list=[email],
                fail_silently=False,
            )