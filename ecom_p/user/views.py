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

# Load environment variables from .env file in the current directory
load_dotenv()

# Get Twilio phone number from the environment
twilio_phone_number = os.environ.get('TWILIO_PHONE_NUMBER')

# Create a Twilio client
client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])

# Create a Verify service
verify = client.verify.services(os.environ['TWILIO_VERIFY_SERVICE_SID'])




def home(request):
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
        # user=CustomUser.objects.get(email = email)
        # print(user,"1111111111111111111111111111111111")
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid Credentials")
            return redirect("handlelogin")

    

        if  user.is_verified == False:
            messages.error(request,"please varify you mobile number!")
            id = user.id
            print(id,"222222222222222222222222222222222222222222222")
            return redirect("enter_mobile",id)
        try:
            user = CustomUser.objects.get(email = email)
        except:
            messages.error(request,"Invalid Credentials")
            return redirect("handlelogin") 
        myuser = authenticate(request,email=email, password=password)
        if myuser:
               if myuser.is_superuser:
                    # login(request,myuser)
                    messages.success(request,"Login Success")
                    return redirect("admin_page")
               else:
                   login(request,myuser)
                   messages.success(request,"Login success")
                   return redirect("home")
                   
        else:
            messages.error(request,"Account is blocked or Not a user!")
            return redirect("handlelogin")
    return render(request,'register/login.html')

def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success!")
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
        print(phone, "4444444444444444444")
        try:
            user = CustomUser.objects.get(phone=phone)
            print("55555555555555555555555")
            send(phone)
            # return redirect("signup_otp",phone=phone)
            return render(request,"register/otp_phone.html",{"id":user.id, "phone":user.phone},)

        except CustomUser.DoesNotExist:
            return HttpResponse("Please enter a valid phone number")
    return render(request, "register/enter_mobile.html")


# def verify_otp(request):
#     return render(request,"register/verify_otp.html")
