

from django.contrib import admin
from .models import *


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'modified_date', 'is_available')

class BannerAdmin(admin.ModelAdmin):
    list_display = ('banner_image',)

# class VariationAdmin(admin.ModelAdmin):
#     list_display = ('product','variation_category','variation_value','is_active')
#     list_editable = ('is_active',)
#     list_filter = ('product','variation_category','variation_value','is_active')    

# class CartAdmin(admin.ModelAdmin):
#     list_display = ('product',)

# admin.site.register(Variation, VariationAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Banner, BannerAdmin)
# admin.site.register(Cart, CartAdmin)
