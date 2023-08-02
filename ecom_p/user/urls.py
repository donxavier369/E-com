from django.urls import path, re_path
from user  import views

urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.handlesignup,name="handlesignup"),
    path('login',views.handlelogin,name="handlelogin"),
    path('logout',views.handlelogout,name="handlelogout"),
    # path('signup_otp/<int:id>,<str:phone>',views.signup_otp,name="signup_otp"),
    path('otpverification/<int:id>,<str:phone>',views.otpverification,name="otpverification"),
    path('enter_mobile/<int:id>',views.enter_mobile,name="enter_mobile"),
    path('verify_phone',views.verify_phone,name='verify_phone'),
    # path('verify_otp',views.verify_otp,name="verify_otp"),

    # user profile
    path('user_profile/',views.user_profile,name='user_profile'),



]
