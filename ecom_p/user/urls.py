from django.urls import path, re_path
from user  import views

urlpatterns = [
    # path('',views.home,name="home"),
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
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('wishlist/',views.wishlist,name="wishlist"),
    path('add_to_wishlist/<int:variant_id>/',views.add_to_wishlist,name="add_to_wishlist"),
    path('remove_wishlist_item/<int:product_id>/<int:wishlist_id>/',views.remove_wishlist_item,name="remove_wishlist_item"),

    # address mangement
    path('address/',views.address,name="address"),
    path('add_address/',views.add_address,name="add_address"),
    path('edit_address/<int:id>',views.edit_address,name="edit_address"),
    path('delete_address/<int:id>',views.delete_address,name="delete_address"),
    path('set_default/<int:id>',views.set_default,name="set_default"),

    # password  management
    path('forgot_password',views.forgot_password, name="forgot_password"),
    path('password_otpverification/<str:phone>',views.password_otpverification,name="password_otpverification"),
    path('change_password/<str:phone>',views.change_password,name="change_password"),
    path('change_password_profile',views.change_password_profile, name="change_password_profile"),

    # orders
    path('order_detail',views.order_detail, name="order_detail"),
    path('order_detail_view/<uuid:bulk_order_id>',views.order_detail_view,name="order_detail_view"),
    path('cancel_order/<int:order_id>/',views.cancel_order,name="cancel_order"),
    




]
