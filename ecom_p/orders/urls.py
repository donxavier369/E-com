from django.urls import path
from . import views


urlpatterns = [
    # path('place_order/',views.place_order, name='place_order'),
    # path('payments/<int:order_id>', views.payments, name='payments'),
    # path('show_address',views.show_address, name='show_address'),
    path('change_address',views.change_address, name='change_address'),
    path('use_address',views.use_address, name='use_address'),
    path('add_checkout_address',views.add_checkout_address, name='add_checkout_address'),
    path('edit_checkout_address/<int:id>',views.edit_checkout_address, name='edit_checkout_address'),
    path('use_address/<int:id>',views.use_address, name='use_address'),

    # payment   
    # path("order_payment/<str:amount>,<str:name>", views.order_payment, name="order_payment"),
    path("order_payment/<int:coupon_id>/", views.order_payment, name="order_payment"),
    path("callback/", views.callback, name="callback"),
    path("order_summery/<str:bulk_order_id>/", views.order_summery, name='order_summery'),
    path("order_failed/", views.order_failed, name="order_failed"),

]
