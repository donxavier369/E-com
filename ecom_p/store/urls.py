
from django.urls import path
from.import views

urlpatterns = [
    path('',views.home,name="home"),
    path('contact',views.contact,name="contact"),
    path('checkout',views.checkout,name="checkout"),
    path('payment',views.payment,name="payment"),
    path('store',views.store,name="store"),
    path('banner',views.banner,name="banner"),
    path('shop',views.shop,name="shop"),
    path('about',views.about,name="about"),
    path('<slug:category_slug>/',views.store,name="products_by_category"),
    path('<slug:category_slug>/<slug:product_slug>',views.product_details,name="product_details"),



]
