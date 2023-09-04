from django import views
from django.urls import path
from .import views


urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    # path('update_cart_item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('update_quantity', views.update_quantity, name='update_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('wishlist_to_cart/<int:product_id>/<int:variant_id>/',views.wishlist_to_cart,name='wishlist_to_cart'),


  

]
