from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from user.models import CustomUser
from store.models import Product

# Create your views here.

def home(request):
    products = Product.objects.all().filter(is_available=True)
    print(products)
    context = {
        'products': products,
    }
    return render(request,'layouts/index.html',context)



def handlesignup(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("pass1")

        try:
            if CustomUser.objects.get(email = email):
                messages.info(request,"Email is Taken")
                return redirect('handlesignup')
        except:
            pass
        try:
            if CustomUser.objects.get(phone_number = phone):
                messages.info(request,"Phonenumber is Taken")
        except:
            pass        

        myuser = CustomUser.objects.create_user(name=uname,email=email,phone_number=phone,password=password)  
        myuser.save()
        messages.success(request,"Signup Success Please Login!")

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



    