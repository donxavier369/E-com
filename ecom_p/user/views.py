from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from user.models import CustomUser
from store.models import Product
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from carts.views import _cart_id,CartItem
from carts.models import Cart, CartItem
import requests
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
        products = Product.objects.all().filter(is_available=True)
        print(products)
        context = {
            'products': products,
        }
        return render(request,'layouts/index.html',context)
        

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
    try:
        result = verify.verification_checks.create(to=phone, code=code)
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



@login_required(login_url='handlelogin')
def user_profile(request):
    user = CustomUser.objects.get(pk=request.user.pk)
    context = {
        'user': user
    }
    return render(request, 'register/user_profile.html', context)
