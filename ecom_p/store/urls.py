
from django.urls import path
from.import views

urlpatterns = [
    path('',views.index,name="home"),
    path('contact',views.contact,name="contact"),
    path('checkout',views.checkout,name="checkout"),
    path('payment',views.payment,name="payment"),
    path('shop',views.shop,name="shop"),
    path('single',views.single,name="single"),
    path('about',views.about,name="about"),


]
