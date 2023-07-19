from django.urls import path
from user  import views

urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.handlesignup,name="handlesignup"),
    path('login',views.handlelogin,name="handlelogin"),
    path('logout',views.handlelogout,name="handlelogout"),

]
