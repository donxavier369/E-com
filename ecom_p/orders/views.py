from django.http import HttpResponse
import uuid
from django.shortcuts import get_object_or_404, render,redirect
from carts.models import CartItem
from .forms import OrderForm,Order
import datetime
from user.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.models import Profile
from ecom_p.settings import RAZORPAY_KEY_ID,RAZORPAY_KEY_SECRET
from .models import Razorpay_Order
from store.models import Product

# Create your views here.


# import time
# import random
from django.views.decorators.csrf import csrf_exempt
import razorpay
from ecom_p.settings import (
    RAZORPAY_KEY_ID,
    RAZORPAY_KEY_SECRET,
)
from .constant import PaymentStatus
from django.views.decorators.csrf import csrf_exempt
import json
from django.template.loader import render_to_string







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


# order and paymenent

def payments(request,order_id):
    return render(request, 'orders/payments.html')



# def place_order(request, total=0, quantity=0):

#     current_user = request.user
#     cart_items = CartItem.objects.filter(user=current_user)
#     cart_count = cart_items.count()


#     if cart_count <= 0:
#         return redirect('store')

#     grand_total = 0
#     tax = 0

#     for cart_item in cart_items:
#         total += (cart_item.product.product_price * cart_item.quantity)
#         quantity += (cart_item.quantity)

#     tax = (2 * total) / 100
#     grand_total = total + tax

#     if request.method == 'POST':
#         # Get the billing information from the form data
#         full_name = request.POST.get('full_name')
#         phone = request.POST.get('phone')
#         email = request.POST.get('email')
#         address_line_1 = request.POST.get('address_line_1')
#         pincode = request.POST.get('pincode')
#         state = request.POST.get('state')
#         city = request.POST.get('city')
#         payment_type = request.POST.get('payment')
#         print(payment_type,"typeeeeeeeeeeeeeeeeeee")
#         if payment_type == "razorpay":
#             print(255)
#             amount = str(grand_total)
#             name = full_name
#             return redirect('order_payment',amount=amount,name=name)

#         # Store all the billing information inside Order table
#         data = Order(
#         user = current_user,
#         full_name = full_name,
#         phone = phone,
#         email = email,
#         address_line_1 = address_line_1,
#         pincode = pincode,
#         state = state,
#         city = city,
#         order_total = grand_total,
#         tax = tax,
#         ip = request.META.get('REMOTE_ADDR'),
#         payment_method = payment_type
          
#         )
#         data.save()
#         cart_items.delete()



#         # Generate order_number
#         yr = int(datetime.date.today().strftime('%Y'))
#         dt = int(datetime.date.today().strftime('%d'))
#         mt = int(datetime.date.today().strftime('%m'))
#         d = datetime.date(yr, mt, dt)
#         current_date = d.strftime('%Y%m%d')  # 20230731
#         order_number = current_date + str(data.id)
#         data.order_number = order_number
#         data.save()

#         # Redirect to payments page with the order details
#         # return redirect('payments', order_id=data.id)
#         return redirect('home')

#     else:
#         return render(request, 'orders/checkout.html', {'total': total, 'tax': tax, 'grand_total': grand_total})



# # manage payment


# def order_payment(request, amount, name):
#     name = name
#     amount = float(amount)
#     client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
#     print(client,"clienttttttttttttttttt")
#     razorpay_order = client.order.create(
#         {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
#     )
#     print(razorpay_order)
#     order = Razorpay_Order.objects.create(
#         name=name, amount=amount,
#         provider_order_id =razorpay_order["id"],
#     )
#     order.save()

#     print(order,"000000000000000")
#     return render(
#         request,
#         "orders/payment.html",
#         {
#             "callback_url": "http://" + "127.0.0.1:8000" + "/orders/callback/",
#             "razorpay_key": RAZORPAY_KEY_ID,
#             "order": order,
#         },
#     )
#     return render(request, "orders/payment.html")





# @csrf_exempt
# def callback(request):
#     print("callllllllllllllll")
#     def verify_signature(response_data):
#         client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
#         return client.utility.verify_payment_signature(response_data)
#     print(request)
#     print(request.POST)
#     if "razorpay_signature" in request.POST:
#         payment_id = request.POST.get("razorpay_payment_id", "")
#         provider_order_id = request.POST.get("razorpay_order_id", "")
#         signature_id = request.POST.get("razorpay_signature", "")
#         order = Razorpay_Order.objects.get(provider_order_id=provider_order_id)
#         order.payment_id = payment_id
#         order.signature_id = signature_id
#         order.save()
#         if verify_signature(request.POST):
#             order.status = PaymentStatus.SUCCESS
#             order.save()
            

#             return render(request, "orders/order_success.html", context={"status": order.status})
        
#         else:
#             order.status = PaymentStatus.FAILURE
#             order.save()
#             return render(request, "orders/order_success.html", context={"status": order.status})
#     else:
#         payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
#         provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
#             "order_id"
#         )
#         order = Order.objects.get(provider_order_id=provider_order_id)
#         order.payment_id = payment_id
#         order.status = PaymentStatus.FAILURE
#         order.save()
#         return render(request, "orders/callback.html", context={"status": order.status})



def place_order(request, total=0, quantity=0):

    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()


    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.product_price * cart_item.quantity)
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
        payment_type = request.POST.get('payment')
        print(payment_type,"typeeeeeeeeeeeeeeeeeee")
        if payment_type == "razorpay":
            print(255)
            amount = str(grand_total)
            name = full_name
            return redirect('order_payment',amount=amount,name=name)

        # Store all the billing information inside Order table
        data = Order(
        user = current_user,
        full_name = full_name,
        phone = phone,
        email = email,
        address_line_1 = address_line_1,
        pincode = pincode,
        state = state,
        city = city,
        order_total = grand_total,
        tax = tax,
        ip = request.META.get('REMOTE_ADDR'),
        payment_method = payment_type
        )
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



# manage payment
# amount, name

def generate_bunch_order_id():
    return str(uuid.uuid4())

def order_payment(request, total=0, quantity=0):

    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()


    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.product_price * cart_item.quantity)
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
        payment_type = request.POST.get('payment')
        print(payment_type,"typeeeeeeeeeeeeeeeeeee")

        bulk_order_id = generate_bunch_order_id()
        print(bulk_order_id)
        if payment_type == "cod":
            
            # Store all the billing information inside Order table
            for cart in cart_items:
                data = Order(
                user = current_user,
                full_name = full_name,
                phone = phone,
                email = email,
                address_line_1 = address_line_1,
                pincode = pincode,
                state = state,
                city = city,
                order_total = grand_total,
                tax = tax,
                ip = request.META.get('REMOTE_ADDR'),
                payment_method = payment_type,
                product_id = cart.product.id,
                variant_id = cart.variant.id,
                quantity= cart.quantity,
                bulk_order_id = bulk_order_id,
                unit_amount = cart.product.product_price,
                total_amount = grand_total
                )
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

        elif payment_type == "razorpay":
            print(255)
            amount = str(grand_total)
            name = full_name
       
            amount = float(amount)
            client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
            print(client,"clienttttttttttttttttt")
            razorpay_order = client.order.create(
                {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
            )
            print(razorpay_order)
            order = Razorpay_Order.objects.create(
                name=name, amount=amount,
                provider_order_id =razorpay_order["id"],
            )
            order.save()

           # Store all the billing information inside Order table
            for cart in cart_items:
                data = Order(
                user = current_user,
                full_name = full_name,
                phone = phone,
                email = email,
                address_line_1 = address_line_1,
                pincode = pincode,
                state = state,
                city = city,
                order_total = grand_total,
                tax = tax,
                ip = request.META.get('REMOTE_ADDR'),
                payment_method = payment_type,
                product_id = cart.product.id,
                variant_id = cart.variant.id,
                quantity= cart.quantity,
                bulk_order_id = bulk_order_id,
                unit_amount = cart.product.product_price,
                total_amount = grand_total
                )
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

            current_order = bulk_order_id
            print(order,"000000000000000")
            return render(
                request,
                "orders/payment.html",
                {
                    "callback_url": "http://" + "127.0.0.1:8000" + "/orders/callback/?current_order={current_order}",
                    "razorpay_key": RAZORPAY_KEY_ID,
                    "order": order,
                },
            )
        else:
            pass
    return render(request, "orders/payment.html")





@csrf_exempt
def callback(request):
    current_order = request.GET.get("current_order")
    print(current_order,"00000000000000")
    current_order = Order.objects.filter(bulk_order_id = current_order)
    print("callllllllllllllll")
    def verify_signature(response_data):
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)
    print(request)
    print(request.POST)
    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Razorpay_Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            
            current_order.payment_status = "Payed"

            return render(request, "orders/order_success.html", context={"status": order.status})
        
        else:
            order.status = PaymentStatus.FAILURE
            order.save()

            return render(request, "orders/order_success.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "orders/callback.html", context={"status": order.status})

