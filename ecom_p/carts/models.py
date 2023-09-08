from django.db import models
from store.models import Product,Variant
from user.models import CustomUser


# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    crated_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    cart_price = models.IntegerField(default=0)

    def sub_total(self):
        return self.product.price * self.quantity
    
    def get_total_quantity(self):
        return sum(item.quantity for item in self.cart.all())

    def __unicode__(self) -> str:
        return self.product
    

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_price = models.IntegerField()
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(default = True)
    end_date = models.DateField(default=0)
    min_price = models.IntegerField(default=0)
    max_price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.discount_price)