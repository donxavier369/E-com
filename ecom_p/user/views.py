from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from carts.views import _cart_id
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from user.models import CustomUser
from store.models import Product,Wishlist,Variant
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv
import os
from twilio.rest import Client
# from carts.views import _cart_id,CartItem
from carts.models import Cart, CartItem
import requests
from .models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from orders.models import Order,Wallet
# Load environment variables from .env file in the current directory
load_dotenv()

# Get Twilio phone number from the environment
# twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')

# Create a Twilio client
client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])

# Create a Verify service
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])




    

@never_cache
def handlesignup(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        phone = '+91'+request.POST.get("phone")
        password = request.POST.get("pass1")

        try:
            if CustomUser.objects.get(email = email):
                messages.info(request,"Email is Taken")
                return redirect('handlesignup')
        except:
            pass
        try:
            if CustomUser.objects.filter(phone = phone):
                messages.info(request,"Phonenumber is Taken")
                return redirect('handlesignup')
        except :
            pass

        try:
            if phone:
                print(phone,"phoneeeeeeeeeeeeeeeeeee")
                send(phone)
                # return redirect("signup_otp",phone=phone)
            else:
                return HttpResponse("Check your internet connection!")
        except:
            pass
                
        myuser = CustomUser.objects.create_user(name=uname,email=email,phone=phone,password=password)  
        myuser.save()
        return render(request,"register/otp_phone.html",{"id":myuser.id, "phone":myuser.phone},)
    return render(request,"register/signup.html")

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart    




@ never_cache
def handlelogin(request):
    
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("pass1")
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid Credentials")
            return redirect("handlelogin")

    

        if  user.is_verified == False:
            messages.error(request,"please varify you mobile number!")
            id = user.id
            return redirect("enter_mobile",id)
        try:
            user = CustomUser.objects.get(email = email)
        except:
            messages.error(request,"Invalid Credentials")
            return redirect("handlelogin") 
        myuser = authenticate(username=email, password=password)
        print(myuser,"haiiiiiiii")
        if myuser:
            print("888888888888888")
            if myuser.is_superuser:
                login(request,myuser)
                # messages.success(request,"Login Success")
                return redirect("admin_page")
            else:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    cart_items = CartItem.objects.filter(cart=cart)

                    for item in cart_items:
                        item.user = myuser
                        item.save()

                except Cart.DoesNotExist:
                    pass
                
                login(request,myuser)

            return redirect('home')

        else:
            messages.error(request, "Account is blocked or not a user!")
            return redirect("handlelogin")
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("admin_page")
        else:
            return redirect("/")
    else:
        return render(request, 'register/login.html')


def handlelogout(request):
    logout(request)
    products = Product.objects.filter(new_arrival=True)
    print(products)
    context = {
        'products':products
    }
    
    return render(request,'layouts/index.html',context)



def send(phone):
    print(phone,"successfully sended")
    verify.verifications.create(to=phone, channel='sms')



def check(phone, code):
    print(phone,'checkkkkkkkkkkkkkkkkk')
    try:
        result = verify.verification_checks.create(to=phone, code=code)
        print('yes')
    except TwilioRestException:
        print('no')
        return False
    return result.status == 'approved'

# def signup_otp(request):
#     return render(request,"register/otp_phone.html")



def otpverification(request,id,phone):
    print(phone,"111111111111111111")
    if request.method == 'POST':
        code = request.POST.get('code')
        if check(phone,code):
           user = CustomUser.objects.filter(id=id).update(is_verified=True)
           
           messages.success(request,"Signup successful please login")
           return redirect("handlelogin")
        else:
            user = CustomUser.objects.get(id=id)
            user.delete()
            return redirect("handlesignup")
        
    return render(request, "register/otp_phone.html")    

def enter_mobile(request,id):
    user = CustomUser.objects.get(id=id)
    context={
        'user':user,
    }
    return render(request, "register/enter_mobile.html", context)

def verify_phone(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        
        try:
            user = CustomUser.objects.get(phone=phone)
            send(phone)
            print('phoneeeeeeeeeeeeeeeeeeeee',phone)
            # return redirect("signup_otp",phone=phone)
            return render(request,"register/otp_phone.html",{"id":user.id, "phone":user.phone},)

        except CustomUser.DoesNotExist:
            return HttpResponse("Please enter a valid phone number")
    return render(request, "register/enter_mobile.html")


# def verify_otp(request):
#     return render(request,"register/verify_otp.html")


# profile management

@login_required(login_url='handlelogin')
def user_profile(request, wallet = 0):
    bool = True
    user = CustomUser.objects.get(pk=request.user.pk)
    try:
        wallet = Wallet.objects.get(user=request.user)
    except:
        pass
    print(wallet,"walllllllllllllll")
    context = {
        'user': user,
        'show_footer': bool,
        'wallet':wallet,
    }
    return render(request, 'Profile/user_profile.html', context)


def edit_profile(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        print(name,"nameeeee")
        print(email,"emaiiiiiiiiiiiiii")
        current_user = request.user
        user = CustomUser.objects.get(id=current_user.id)
        user.name = name
        user.email = email
        user.phone = phone
        user.save()
 
        return redirect('user_profile')
    return render(request, 'Profile/user_profile.html')

# address management

def address(request):
    bool = True

    addresses = Profile.objects.filter(user=request.user)
    context = {
        'show_footer': bool,
        'addresses':addresses
    }
    
    return render(request, 'Profile/address.html',context)



def add_address(request):
    if request.method == 'POST':
        name = request.POST.get('user_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        city = request.POST.get('city')
        user = CustomUser.objects.get(id = request.user.id)
        profile = Profile(
            full_name = name,
            phone = phone,
            email = email,
            address_line_1 = address,
            pincode = pincode,
            state = state,
            city = city,
            user = user,
        )
        check_address = Profile.objects.filter(user=request.user)
        if check_address:
            profile.save()
        else:
            profile.set_default = True
            profile.save()    
        messages.success(request,"Your address has been added successfully")
        return redirect('address')

    return render(request,'Profile/address.html')

@login_required(login_url='handlelogin')
def edit_address(request,id):
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
        messages.success(request, "Your address has been successfully edited")
        return redirect('address')

    return render(request,'Profile/address.html')


def delete_address(request, id):
    if request.method == 'POST':
        del_address = Profile.objects.get(id=id, user=request.user)
        print(del_address,"del addressssssssss")
        if del_address.set_default == True:
            del_address.delete()
            set_another_default = Profile.objects.filter(user=request.user)
            print(address)
            if set_another_default:
                set_another_default[0].set_default = True
                set_another_default[0].save()
        else:
            del_address.delete()
        messages.info(request, "Your selected address has been successfully deleted.")
        return redirect('address')
    return redirect('address')
 

def set_default(request, id):
    if request.method == 'POST':
        address = Profile.objects.get(user=request.user,id=id)
        address.set_default = True
        address.save()
        
        try:
            defaults_to_reset = Profile.objects.filter(set_default=True).exclude(user=request.user, id=id)
            for default_address in defaults_to_reset:
                default_address.set_default = False
                default_address.save()
        except Profile.DoesNotExist:
            pass
        messages.success(request, "Your selected address has been set as the default for your future product purchases.")
        return redirect('address')
    return render(request,'profile/address.html' )


# password management

def forgot_password(request):
    
    if request.method == 'POST':
        phone = '+91'+request.POST.get("phone")

        try:
            if phone:
                print(phone,'otp send')
                send(phone)
            else:
                HttpResponse("Check Your Internet Connection!")
        except:
            pass            
        context={
            'phone':phone
        }
        return render(request,'Profile/Enter_otp_password.html',context)
    return render(request,'Profile/forgot_password.html')


def password_otpverification(request,phone):
    if request.method == 'POST':
        code = request.POST.get('code')

        if check(phone,code):
            user = CustomUser.objects.filter(phone=phone)
            try:
              if user:
                return redirect("change_password",phone=phone)
            except:
               HttpResponse('enter currect phone number')  
        else:
            return render(request, "Profile/Enter_otp_password.html",{'phone':phone})
    return render(request, "Profile/Enter_otp_password.html",{'phone':phone})


def change_password(request,phone):
    print(phone,'done')
    if request.method == 'POST':
        new_password = request.POST.get('new_password1')
        print(new_password)
        user = CustomUser.objects.get(phone=phone)

        if user.password == new_password:
            messages.success(request,"This password similar to your old password")
            return render(request,"Profile/change_password.html",{'phone':phone})
        else:
            update_password=CustomUser.objects.filter(id=user.id).update(password=make_password(new_password))

        

        messages.success(request,"Password changed successfulley")
        return redirect('handlelogin')                

  
    return render(request,"Profile/change_password.html",{'phone':phone})


def change_password_profile(request):
    if request.method == 'POST':
        password = request.POST.get('new_password')
        print(password,"22222222222")
        user = request.user
        current_user = CustomUser.objects.get(id = user.id)
        current_password = current_user.password
        try:
            current_password == password
            messages.info(request,"This password is you old password")
        except:
            pass
        current_user.password = make_password(password)
        current_user.save()
        messages.success(request,"password changes successfully")
        return redirect('user_profile')

    return render(request, 'Profile/user_profile.html')




# orders

def order_detail(request):
    bool = True
    orders = Order.objects.filter(user=request.user,)
    print(orders,"ooooooooooooooooo ")


    context = {
        'show_footer': bool,
        'orders':orders,

    }
    return render(request,"profile/order_detail.html",context)

def order_detail_view(request,bulk_order_id, price=0):
    print(bulk_order_id,"bulk KKKKKKKKKK")
    bool = True
    orders = Order.objects.filter(bulk_order_id = bulk_order_id)
    order = Order.objects.filter(bulk_order_id=bulk_order_id).first()
    print(orders,"ordersssssssssssssss")
    
    for ord in orders:
        price += int(ord.unit_amount)
   
    context = {
        'show_footer': bool,
        'orders':orders,
        'order':order,
        'price':price,
       
    }
    return render(request,"profile/order_detail_view.html",context )

def cancel_order(request,order_id):
    current_order = Order.objects.get(order_number=order_id)
    current_order.status = "Cancelled"  
    current_order.save() 
    cancel_order_price = int(current_order.unit_amount)
    print(cancel_order_price,"11111111111111")
    try:
        wallet = Wallet.objects.filter(user=request.user).first()
        print(wallet,"2222222222222")
    except:
        pass

    if wallet is None:
        wallet = Wallet.objects.create(user=request.user, wallet_amount = 0)
        print(wallet,"333333333333")


    wallet.wallet_amount += cancel_order_price 
    print(wallet.wallet_amount,"44444444444444")
    wallet.save()
    bulk_order_id = current_order.bulk_order_id
    print(current_order.status,"cancelledddddddddddddddd")
    return redirect(order_detail_view,bulk_order_id)


# wishlist

@login_required(login_url='handlelogin')
def wishlist(request):
    wishlists = Wishlist.objects.all()
    bool = True
    context = {
        'wishlists':wishlists,
        'show_footer': bool,
    }
    return render(request,"profile/wishlist.html",context)

@login_required(login_url='handlelogin')
def add_to_wishlist(request,variant_id):
    variant = get_object_or_404(Variant, id=variant_id)
    print(variant_id,"varianttttttttttttt")
    product = variant.product
    wishlist_entry = Wishlist.objects.filter(user=request.user, variant = variant).first()
    print("productttttt",product)
    if wishlist_entry:
        messages.info(request,"Product already in wishlist")
    else:
        Wishlist.objects.create(
            product = product,
            variant = variant,
            user=request.user,
        
        )
        messages.info(request,"Product added to wishlist")
        # return redirect('wishlist')
    return redirect('product_details',productid=product.id)

# def add_to_wishlist_ajax(request, productid):
#     product = get_object_or_404(Product, id=productid)
    
#     wishlist_entry = Wishlist.objects.filter(user=request.user, product=product).first()
    
#     if wishlist_entry:
#         response_data = {'message': 'already_in_wishlist'}
#     else:
#         Wishlist.objects.create(
#             product=product,
#             user=request.user,
#         )
#         response_data = {'message': 'added_to_wishlist'}
    
#     return JsonResponse(response_data)

def remove_wishlist_item(request, product_id, wishlist_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        wishlist_item = Wishlist.objects.get(product=product, user=request.user, id=wishlist_id)
        wishlist_item.delete()

    else:
        pass
    
    return redirect('wishlist')

