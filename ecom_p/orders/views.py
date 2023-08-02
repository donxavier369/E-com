from django.http import HttpResponse
from django.shortcuts import render,redirect
from carts.models import CartItem
from .forms import OrderForm,Order
import datetime
from user.models import CustomUser
from django.contrib.auth.decorators import login_required
# Create your views here.


def payments(request,order_id):
    return render(request, 'orders/payments.html')

# def place_order(request, total=0, quantity=0):
#     current_user = request.user
#     #if the cart count is less than or equal to 0, then redirect back to shop
#     cart_item = CartItem.objects.filter(user=current_user)
#     cart_count = cart_item.count()
#     if cart_count <= 0:
#         return redirect('store')

#     grand_total = 0
#     tax = 0
#     for cart_item in CartItem:
#         total += (cart_item.product.price * cart_item.quantity)
#         quantity += (cart_item.quantity)
#     tax = (2 * total)/100
#     grand_total = total * tax     
      
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             # store all the billing information inside Order table
#             data = Order()
#             data.user = current_user
#             data.first_name = form.cleaned_data['first_name']
#             data.last_name = form.cleaned_data['last_name']
#             data.phone = form.cleaned_data['phone']
#             data.email = form.cleaned_data['email']
#             data.address_line_1 = form.cleaned_data['address_line_1']
#             data.adress_line_2 = form.cleaned_data['address_line_2']
#             data.country = form.cleaned_data['country']
#             data.state = form.cleaned_data['state']
#             data.city = form.cleaned_data['city']
#             data.order_note = form.cleaned_data['order_note']
#             data.order_total = grand_total
#             data.tax = tax
#             data.ip = request.META.get('REMOTE_ADDR')
#             data.save()
#             # generate order_number
#             yr = int(datetime.date.today().strftime('%Y'))
#             dt = int(datetime.data.today().strftime('%d'))
#             mt = int(datetime.date.today().strftime('%m'))
#             d = datetime.date(yr,mt,dt)
#             current_date = d.strftime('%Y%m%d') #20230731
#             order_number = current_date + str(data.id)
#             data.order_number = order_number
#             data.save()
#             return redirect('payments')
#     else:
#         return redirect('checkout')



# def place_order(request, total=0, quantity=0):
#     current_user = request.user
#     cart_items = CartItem.objects.filter(user=current_user)
#     cart_count = cart_items.count()

#     if cart_count <= 0:
#         return redirect('store')

#     grand_total = 0
#     tax = 0

#     for cart_item in cart_items:
#         total += (cart_item.product.price * cart_item.quantity)
#         quantity += (cart_item.quantity)

#     tax = (2 * total) / 100
#     grand_total = total + tax

#     if request.method == 'POST':
#         print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             data = Order()
#             data.user = current_user
#             data.first_name = form.cleaned_data['first_name']
#             data.last_name = form.cleaned_data['last_name']
#             data.phone = form.cleaned_data['phone']
#             data.email = form.cleaned_data['email']
#             data.address_line_1 = form.cleaned_data['address_line_1']
#             data.address_line_2 = form.cleaned_data['address_line_2']
#             data.country = form.cleaned_data['country']
#             data.state = form.cleaned_data['state']
#             data.city = form.cleaned_data['city']
#             data.order_note = form.cleaned_data['order_note']
#             data.order_total = grand_total
#             data.tax = tax
#             data.ip = request.META.get('REMOTE_ADDR')
#             data.save()

#             # Generate order_number
#             yr = int(datetime.date.today().strftime('%Y'))
#             dt = int(datetime.date.today().strftime('%d'))
#             mt = int(datetime.date.today().strftime('%m'))
#             d = datetime.date(yr, mt, dt)
#             current_date = d.strftime('%Y%m%d')  # 20230731
#             order_number = current_date + str(data.id)
#             data.order_number = order_number
#             data.save()
                    
#             # Redirect to payments page with the order details
#             return redirect('payments', order_id=data.id)

#     else:
#         form = OrderForm()

#     context = {
#         'form': form,
#         'total': total,
#         'tax': tax,
#         'grand_total': grand_total,
#     }
#     return render(request, 'store/checkout.html', context)



def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += (cart_item.quantity)

    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        # Get the billing information from the form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        order_note = request.POST.get('order_note')

        # Store all the billing information inside Order table
        data = Order()
        data.user = current_user
        data.first_name = first_name
        data.last_name = last_name
        data.phone = phone
        data.email = email
        data.address_line_1 = address_line_1
        data.address_line_2 = address_line_2
        data.country = country
        data.state = state
        data.city = city
        data.order_note = order_note
        data.order_total = grand_total
        data.tax = tax
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()
        cart_items.delete()

        # Generate order_number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime('%Y%m%d')  # 20230731
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()

        # Redirect to payments page with the order details
        return redirect('payments', order_id=data.id)

    else:
        return render(request, 'store/checkout.html', {'total': total, 'tax': tax, 'grand_total': grand_total})




