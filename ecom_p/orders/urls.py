from django.urls import path
from . import views


urlpatterns = [
    path('place_order/',views.place_order, name='place_order'),
    path('payments/<int:order_id>', views.payments, name='payments'),
]
