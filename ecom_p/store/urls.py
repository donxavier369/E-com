
from django.urls import path
from.import views

urlpatterns = [
    path('',views.home,name="home"),
    path('contact',views.contact,name="contact"),
    # path('checkout',views.checkout,name="checkout"),
    # path('payment',views.payment,name="payment"),
    path('store',views.store,name="store"),
    path('banner',views.banner,name="banner"),
    # path('shop',views.shop,name="shop"),
    path('about',views.about,name="about"),
    path('store',views.store,name="store"),
    path('product_details/<int:productid>',views.product_details,name="product_details"),
    path('categories/<int:categoryid>',views.categories, name="categories"),
    path('get-variant-details', views.get_variant_details, name='get-variant-details'),
    
]
