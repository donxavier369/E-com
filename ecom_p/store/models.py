
         
from django.db import models
from category.models import *
from django.urls import reverse
from user.models import CustomUser

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    new_arrival = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_details', args=[self.category.pk, self.pk])

    def __str__(self):
        return self.product_name

class Banner(models.Model):
    banner_image = models.ImageField(upload_to='photos/products')


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False,blank=False)
    create_at = models.DateTimeField(auto_now_add=True)


