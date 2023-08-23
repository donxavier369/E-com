from django.db import models
from django.utils import timezone
from user.models import CustomUser
from store.models import Product,Variant
    
from django.db import models
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constant import PaymentStatus

# Create your models here.

    
class Order(models.Model):
    STATUS = (
        ('Ordered', 'Ordered'),
        ('Approved', 'Approved'),
        ('Shipped', 'Shipped'),     
        ('Returned', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )    

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)    
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, default=None)
    order_number = models.CharField(max_length=20)
    bulk_order_id = models.CharField(max_length=100,default=None)
    total_amount = models.CharField(default=0)
    unit_amount = models.CharField(default=0)
    payment_method = models.CharField(default=0)
    payment_status = models.CharField(max_length=100, default="Not Paid")
    is_canceled = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    pincode = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='Ordered')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)    
    updated_at = models.DateTimeField(default=timezone.now)   
    

    def __str__ (self):
        return self.full_name
    
# class Payment(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     payment_id = models.CharField(max_length=100)
#     payment_method = models.CharField(max_length=100)
#     amount_paid = models.CharField(max_length=100) # this is the total amount paid
#     status = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:
#         return self.payment_id


# class OrderProduct(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     # variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
#     color = models.CharField(max_length=50)
#     quantity = models.IntegerField()
#     product_price = models.FloatField()
#     ordered = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateField(auto_now=True) 

#     def __str__(self) -> str:
#         return self.product.product_name 
    

    

class Razorpay_Order(models.Model):
    name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"
