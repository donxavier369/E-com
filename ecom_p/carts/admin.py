from django.contrib import admin
from .models import Cart, CartItem,Coupon
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product','cart','quantity','is_active')

class CouponAdmin(admin.ModelAdmin):
    list_display = ('code','discount_price','is_active','start_date','end_date','min_price','max_price')

admin.site.register(Coupon,CouponAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)
