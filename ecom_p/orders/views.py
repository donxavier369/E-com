from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from carts.models import CartItem
from .forms import OrderForm,Order
import datetime
from user.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.models import Profile
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
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address_line_1 = request.POST.get('address_line_1')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        city = request.POST.get('city')

        # Store all the billing information inside Order table
        data = Order()
        data.user = current_user
        data.full_name = full_name
        data.phone = phone
        data.email = email
        data.address_line_1 = address_line_1
        data.pincode = pincode
        data.state = state
        data.city = city
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
        # return redirect('payments', order_id=data.id)
        return redirect('home')

    else:
        return render(request, 'orders/checkout.html', {'total': total, 'tax': tax, 'grand_total': grand_total})




def change_address(request):
    addresses = Profile.objects.filter(user=request.user)
    context = {
        'addresses':addresses
    }
    return render(request,'orders/checkout_address.html',context)



def use_address(request,id):
    total_address = Profile.objects.all(user=request.user).count()
    context={ 'total_address':total_address }
    if total_address <= 1:
        address = Profile.objects.get(user=request.user, id=id)
        address.set_default = True
        address.save()
        


    if request.method == 'POST':
        address = Profile.objects.get(user=request.user, id=id)
        address.set_default = True
        address.save()

        try:
            use_address = Profile.objects.filter(set_default=True).exclude(user=request.user, id=id)
            for set_use_address in use_address:
                set_use_address.set_default = False
                set_use_address.save()
        except use_address.DoesNotExist:
            pass
        return redirect('change_address')
    return render(request, 'orders/checkout_address.html', context)


def add_checkout_address(request):
    if request.method == 'POST':
        name = request.POST.get('user_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        city = request.POST.get('city')
        user = CustomUser.objects.get(id = request.user.id)
        profile = Profile.objects.create(
            full_name = name,
            phone = phone,
            email = email,
            address_line_1 = address,
            pincode = pincode,
            state = state,
            city = city,
            user = user,
        )

        return redirect('change_address')

    return render(request,'orders/checkout_address.html')


def edit_checkout_address(request,id):
    address = get_object_or_404(Profile, id=id)
    if request.method == 'POST':
        address_name = request.POST.get('name')
        address_phone = request.POST.get('phone')
        address_email = request.POST.get('email')
        address_address = request.POST.get('address')
        address_pincode = request.POST.get('pincode')
        address_state = request.POST.get('state')
        address_city = request.POST.get('city')

        address.full_name = address_name
        address.phone = address_phone
        address.email = address_email
        address.address_line_1 = address_address
        address.country = address_pincode
        address.state = address_state
        address.city = address_city
        print(address_city)
        address.save()
        return redirect('change_address')

    return render(request,'orders/checkout_address.html')

def use_address(request, id):
    print("111111111111111111111111111")

    if request.method == 'POST':
        address = Profile.objects.get(user=request.user,id=id)
        address.set_default = True
        address.save()
        print(address,"111111111111111111111111111")
        
        try:
            defaults_to_reset = Profile.objects.filter(set_default=True).exclude(user=request.user, id=id)
            for default_address in defaults_to_reset:
                default_address.set_default = False
                default_address.save()
        except Profile.DoesNotExist:
            pass
      
        return redirect('change_address')
    return render(request,'orders/checkout_address.html' )
