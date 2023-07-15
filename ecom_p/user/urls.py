
from django.urls import path
from.import views

urlpatterns = [
    path('login/',views.handlelogin,name="handlelogin"),
    path('signup/',views.handlesignup,name="handlesignup")

]
