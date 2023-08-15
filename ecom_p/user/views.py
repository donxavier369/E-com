from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
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
from twilio.base.exceptions import TwilioRestException
# from carts.views import _cart_id,CartItem
from carts.models import Cart, CartItem
import requests
from .models import Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from orders.models import Order
# Load environment variables from .env file in the current directory
load_dotenv()

# Get Twilio phone number from the environment
twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')

# Create a Twilio client
client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])

# Create a Verify service
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])





def home(request):
    if request.user.is_authenticated and request.user.is_superuser==False:
        products = Product.objects.all().filter(is_available=True)
        print(products)
        context = {
            'products': products,
           
        }
        return render(request,'layouts/index.html',context)
    else:
        logout(request)
        request.session.flush()
        return render(request,'layouts/index.html')        

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
                print(phone)
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

@ never_cache
def handlelogin(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("admin_page")
        else:
            return redirect("/")
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
        myuser = authenticate(request,email=email, password=password)
        if myuser:
                if myuser.is_superuser:
                    login(request,myuser)
                    # messages.success(request,"Login Success")
                    return redirect("admin_page")
                else:
                    try:
                       cart = Cart.objects.get(cart_id=_cart_id(request))
                       is_cart_item_exist = CartItem.objects.filter(cart=cart).exists()
                       print(is_cart_item_exist)
                       if is_cart_item_exist:
                           cart_item = CartItem.objects.filter(cart=cart)
 
                           # getting the product variation by cart id
                           product_variation = []
                           for item in cart_item:
                               variation = item.variations.all()
                               product_variation.append(list(variation))

                           # Get the cart items from the usr ot access his product variations
                           cart_item = CartItem.objects.filter(user = myuser)
                           ex_var_list = []
                           id = []
                           for item in cart_item:
                                existing_variation = item.variations.all()
                                ex_var_list.append(list(existing_variation))
                                id.append(item.id)
    

                        #    product_variation = [1,2,3,5,6]
                        #    ex_var_list = [4,6,3,5]

                           for pr in product_variation:
                            if pr in ex_var_list:
                               index = ex_var_list.index(pr)
                               item_id = id[index]
                               item = CartItem.objects.get(id=item_id)
                               item.quantity += 1
                               item.user = user
                               item.save
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = myuser
                                    item.save()

                    except:
                       print('enetereing inside the except block ')
                       pass    
                    login(request,myuser)
                #    messages.success(request,"Login success") 
                    url = request.META.get('HTTP_REFERER')
                    try:
                       query = requests.utils.urlparse(url).query
                       # next=/cart/checkout/
                       params = dict(x.split('=') for x in query.split('&'))
                       if 'next' in params:
                           nextPage = params['next']
                           return redirect(nextPage)
                    except:
                       return redirect("home")
                   
        else:
            messages.error(request,"Account is blocked or Not a user!")
            return redirect("handlelogin")
    return render(request,'register/login.html')

def handlelogout(request):
    logout(request)
    # messages.info(request,"Logout Success!")
    return redirect('home') 



def send(phone):
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
            # return redirect("signup_otp",phone=phone)
            return render(request,"register/otp_phone.html",{"id":user.id, "phone":user.phone},)

        except CustomUser.DoesNotExist:
            return HttpResponse("Please enter a valid phone number")
    return render(request, "register/enter_mobile.html")


# def verify_otp(request):
#     return render(request,"register/verify_otp.html")


# profile management

@login_required(login_url='handlelogin')
def user_profile(request):
    bool = True
    user = CustomUser.objects.get(pk=request.user.pk)
    context = {
        'user': user,
        'show_footer': bool
    }
    return render(request, 'Profile/user_profile.html', context)


def detail_profile(request):
    bool = True
    user = CustomUser.objects.get(pk=request.user.pk)
    context = {
        'user': user,
        'show_footer': bool
    }
    return render(request, 'Profile/detail_profile.html',context)

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
        return redirect('address')

    return render(request,'Profile/address.html')


def delete_address(request, id):
    if request.method == 'POST':
        del_address = Profile.objects.get(id=id, user=request.user)
        if del_address.set_default == True:
            del_address.delete()
            set_another_default = Profile.objects.filter(user=request.user)
            print(address)
            if set_another_default:
                set_another_default[0].set_default = True
                set_another_default[0].save()
        else:
            del_address.delete()
           
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



# orders

def order_detail(request):
    bool = True
    orders = Order.objects.filter(user=request.user)
    print(orders,"ooooooooooooooooo ")


    context = {
        'show_footer': bool,
        'orders':orders,

    }
    return render(request,"profile/order_detail.html",context)

# wishlist

def wishlist(request):
    wishlists = Wishlist.objects.all()
    bool = True
    context = {
        'wishlists':wishlists,
        'show_footer': bool,
    }
    return render(request,"profile/wishlist.html",context)

def add_to_wishlist(request, product_id):
    print('hello0',product_id)
    product = get_object_or_404(Product, id=product_id)
    variation = Variant.objects.filter(product=product)
    # Check if the product is already in the user's wishlist
    wishlist_entry = Wishlist.objects.filter(user=request.user, product=product).first()
    
    if wishlist_entry:
        messages.info(request,"Product already in wishlist")
    else:
        Wishlist.objects.create(
            product=product,
            user=request.user,
        
        )
        messages.info(request,"Product added to wishlist")
      
        return render(request, 'store/product_detail.html',{"single_product":product}) # Assuming "wishlist" is the URL name for the wishlist page
    return render(request, 'store/product_detail.html',{"single_product":product,"variation":variation})

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

