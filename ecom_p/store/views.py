from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'layouts/index.html')

def contact(request):
    return render(request,'contact.html')

def checkout(request):
    return render(request,'checkout.html')

def payment(request):
    return render(request, 'payment.html')

def shop(request):
    return render(request,"shop.html")

def single(request):
    return render(request,"single.html")

def about(request):
    return render(request,"about.html")

