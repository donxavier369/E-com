from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.urls import reverse
from user.models import CustomUser
from django.contrib.auth import authenticate,login,logout

# Create your views here.


def manageuser(request):
    if request.user.is_authenticated and request.path != reverse('manageuser'):
        return redirect('manageuser')

    data = CustomUser.objects.all()  # Define data here

    if 'search' in request.GET:
        q = request.GET['search']
        data = CustomUser.objects.filter(Q(name__icontains=q) | Q(email__icontains=q) | Q(id__icontains=q))

    context = {'data': data}
    return render(request, "adm/data.html", context)  

def user_block(requset,id):
    d = CustomUser.objects.get(id=id)
    d.is_active = False
    d.save()
    messages.error(requset,"Blcked Successfully")
    return redirect("manageuser")

def user_unblock(request,id):
    d = CustomUser.objects.get(id=id)
    d.is_active = True
    d.save()
    messages.success(request,"Unblock Successfully")
    return redirect("manageuser")

def add(request):
    if request.user.is_authenticated:
        return redirect('manageuser')
    if request.method=="POST":
        email=request.POST.get("email")
        pass1=request.POST.get("pass1")
        myuser = authenticate(email=email,password=pass1)
        if myuser is not None:
            if myuser.is_superuser:
                login(request,myuser)
                messages.success(request,"Login Success!")
                return redirect("manageuser")
            elif myuser is not myuser.is_superuser:
                messages.error(request,"You are not an Admin")
                return redirect('add')
        else:
            messages.error(request,"Invalid Credentials")

    return render(request,"adm/add.html")             
            
def admin_logout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('add')


def admin_page(request):
    return render(request,"Admin/adminindex.html")