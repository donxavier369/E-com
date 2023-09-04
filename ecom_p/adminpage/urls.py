from django.urls import path
from.import views 

urlpatterns = [
    path("manageuser",views.manageuser,name="manageuser"),
    path('user_block/<int:id>/',views.user_block,name="user_block"),
    path('user_unblock/<int:id>/',views.user_unblock,name="user_unblock"),
    path('admin_login',views.admin_login,name="admin_login"),
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

    path('variant/<int:id>', views.variant, name="variant"),
    path('variant_details/<int:id>',views.variant_details, name="variant_details"),
    path('delete_variant/<int:id>', views.delete_variant, name="delete_variant"),

    # user order management
    path('manageorder', views.manage_order, name="manage_order"),
    path('manage_orderstatus/<int:id>',views.manage_orderstatus,name="manage_orderstatus"),

    # coupon managemnt
    path('coupon', views.coupon, name="coupon"),
    path('add_coupon',views.add_coupon, name="add_coupon"),
    path('edit_coupon/<int:coupon_id>/', views.edit_coupon, name="edit_coupon"),
    path('coupon_block/<int:coupon_id>/', views.coupon_block, name="coupon_block"),
    path('coupon_unblock/<int:coupon_id>/', views.coupon_unblock, name="coupon_unblock"),

    # brand management
    path('add_brand', views.add_brand, name="add_brand"),
    path('brand_block/<int:brand_id>/', views.brand_block, name="brand_block"),
    path('brand_unblock/<int:brand_id>/', views.brand_unblock, name="brand_unblock"),
    
    path('sales_report', views.sales_report, name="sales_report"),
]
