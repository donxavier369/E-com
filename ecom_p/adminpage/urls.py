from django.urls import path
from.import views 

urlpatterns = [
    path("manageuser",views.manageuser,name="manageuser"),
    path('block/<id>',views.user_block,name="block"),
    path('unblock/<id>',views.user_unblock,name="unblock"),
    path('add',views.add,name="add"),
    path('admin_logout',views.admin_logout,name="admin_logout"),
    path('admin_page',views.admin_page,name="admin_page"),
    # product management
    path('product',views.product,name="product"),
    path('product/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('product_block/<id>',views.product_block,name="product_block"),
    path('product_unblock/<id>',views.product_unblock,name="product_unblock"),
    path('add_product', views.add_product, name='add_product'),
    # category management
    path('category', views.category, name="category"),
    path('category_block/<id>',views. category_block,name="category_block"),
    path('category_unblock/<id>',views. category_unblock,name="category_unblock"),
    path('add_category', views.add_category,name="add_category"),
    path('category/edit/<int:id>',views.edit_category,name="edit_category"),
    
    # variant management

    path('variant', views.variant, name="variant"),

    # user order management
    path('manageorder', views.manage_order, name="manage_order"),
    path('manage_orderstatus/<int:id>',views.manage_orderstatus,name="manage_orderstatus"),
]
