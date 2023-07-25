# from django.contrib import admin
# from .models import Product,Banner # The model name should start with an uppercase letter

# # Register your models here.
# class ProductAdmin(admin.ModelAdmin):  # Correct the typo here
#     list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')  # Corrected 'catgeory' to 'category'
#     prepopulated_fields = {'slug': ('product_name',)}

# class BannerAdmin(admin.ModelAdmin):
#     list_display = ('banner_image',)    
    
# admin.site.register(Product, ProductAdmin)  # Use correct model name 'Product' here
# admin.site.register(Banner,BannerAdmin)

from django.contrib import admin
from .models import *

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')

class BannerAdmin(admin.ModelAdmin):
    list_display = ('banner_image',)

class CartAdmin(admin.ModelAdmin):
    list_display = ('product',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Cart, CartAdmin)
