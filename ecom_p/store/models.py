
         
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
    # variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_details', args=[self.category.pk, self.pk])

    def __str__(self):
        return self.product_name
    
class variationManager(models.Manager):
    def colors(self):
        return super(variationManager, self).filter(variation_category='color', is_active=True)
    
variation_category_choice = {
    ('color','color')
}    

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)

    objects = variationManager()

    def __str__(self) -> str:
        return self.variation_value

class Banner(models.Model):
    banner_image = models.ImageField(upload_to='photos/products')


