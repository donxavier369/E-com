from django import forms 
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name','phone','email','address_line_1','pincode','state','city']