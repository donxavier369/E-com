from django.contrib import admin
from .models import Category,Brand

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)

admin.site.register(Category, CategoryAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name',)

admin.site.register(Brand,BrandAdmin)   

# class VariantAdmin(admin.ModelAdmin):
#     list_display = ('variant_name',)

# admin.site.register(Variant,VariantAdmin)    