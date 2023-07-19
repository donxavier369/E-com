from django.shortcuts import render,get_object_or_404
from store.models import Product,Banner
from category.models import Category
from django.urls import reverse
from django.http import Http404

# Create your views here.

def home(request):
    products = Product.objects.all().filter(is_available=True)
    print(products)
    context = {
        'products': products,
    }
    return render(request,'layouts/index.html',context)

def contact(request):
    return render(request,'contact.html')

def checkout(request):
    return render(request,'checkout.html')

def payment(request):
    return render(request, 'payment.html')

def about(request):
    return render(request,"about.html")



def shop(request):
    products = Product.objects.all().filter(is_available=True)
    context={
        'products':products
    }
    return render(request,'store/shop.html',context)



def product_details(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug)
    except Exception as e:
        raise e

    context={
        'single_product': single_product
    }    
    return render(request,'store/product_detail.html',context)




def store(request, category_slug=None):
    categories = None
    product = None

    if  category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug)
        product = Product.objects.all().filter(category = categories, is_available = True)
        product_count = products.count()
    else:    
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {
        'products': products,
        'product_count' : product_count,
    }    
    return render(request, 'store/shop.html', context)


def banner(request):
    banners = Banner.objects.all().filter(is_available=True)
    print(banner,"44444444444444444444444444444444444")
    context={
        'banners':banners
    }
    return render(request,'layouts/index.html',context)