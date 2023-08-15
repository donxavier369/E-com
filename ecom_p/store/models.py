
         
from django.db import models
from category.models import Category, Brand
from django.urls import reverse
from user.models import CustomUser



# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    images = models.ImageField(upload_to='photos/products')
    is_available = models.BooleanField(default=True)
    new_arrival = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    product_price = models.IntegerField(default=0)

    def get_url(self):
        return reverse('product_details', args=[self.category.pk, self.pk])

    def __str__(self):
        return self.product_name
    



class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant_colour = models.CharField(max_length=50)
    variant_stock = models.IntegerField(default=0)
    # variant_price = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    variant_image = models.ImageField(upload_to='variant_image')

    def __str__(self) -> str:
        return self.variant_colour  
    
# class variationManager(models.Manager):
#     def colors(self):
#         return super(variationManager, self).filter(variation_category='color', is_active=True)
    
# variation_category_choice = {
#     ('color','color')
# }    

# class Variation(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     variation_category = models.CharField(max_length=100, choices=variation_category_choice)
#     variation_value = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now=True)

#     objects = variationManager()

#     def __str__(self) -> str:
#         return self.variation_value

class Banner(models.Model):
    banner_image = models.ImageField(upload_to='photos/products')



class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE,null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
