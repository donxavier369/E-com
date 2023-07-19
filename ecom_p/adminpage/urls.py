from django.urls import path
from.import views 

urlpatterns = [
    path("manageuser",views.manageuser,name="manageuser"),
    path('block/<id>',views.user_block,name="block"),
    path('unblock/<id>',views.user_unblock,name="unblock"),
    path('add',views.add,name="add"),
    path('admin_logout',views.admin_logout,name="admin_logout"),
    path('admin_page',views.admin_page,name="admin_page"),
]
