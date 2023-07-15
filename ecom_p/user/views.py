from django.shortcuts import render,redirect
from django.contrib import messages
from user.models import Account
from django.db import IntegrityError
# Create your views here.




def handlesignup(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")
        print(phone,"1111111111111111111111")

        if pass1 != pass2:
            messages.warning(request, "Passwords do not match")
            return redirect('handlesignup')

        try:
            # Check if the username already exists
            if Account.objects.filter(username=uname).exists():
                messages.warning(request, "Username already exists")
                return redirect('handlesignup')
            
            # Check if the email already exists
            if Account.objects.filter(email=email).exists():
                messages.warning(request, "Email already exists")
                return redirect('handlesignup')
            
            # Check if the phone number already exists
            if Account.objects.filter(mobile=phone).exists():
                messages.warning(request, "Phone number already exists")
                return redirect('handlesignup')
                
            # Create the user account
            myuser = Account.objects.create(username=uname, email=email, password=pass1, mobile=phone)
            myuser.save()
            messages.success(request, "Signup successful. Please login.")
            # return redirect('handlelogin')

        except IntegrityError:
            messages.error(request, "An error occurred while creating the user account")
            return redirect('handlesignup')

    return render(request, 'register/signup.html')


def handlelogin(request):
    return render(request,"register/login.html")

