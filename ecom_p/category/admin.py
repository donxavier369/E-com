from django.contrib import admin
from .models import Category,Brand
from store.models import Variant

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)

admin.site.register(Category, CategoryAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name',)

admin.site.register(Brand,BrandAdmin)   

class VariantAdmin(admin.ModelAdmin):
    list_display = ('variant_colour','variant_stock')

admin.site.register(Variant,VariantAdmin)    