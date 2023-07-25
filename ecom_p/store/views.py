from django.shortcuts import render,get_object_or_404
from store.models import Product,Banner
from category.models import Category
from django.urls import reverse
from django.http import Http404
from .models import Product, Category

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





def banner(request):
    banners = Banner.objects.all().filter(is_available=True)
    print(banner,"44444444444444444444444444444444444")
    context={
        'banners':banners
    }
    return render(request,'layouts/index.html',context)



def shop(request):
    products = Product.objects.filter(is_available=True)
    context = {
        'products': products
    }
    return render(request, 'store/shop.html', context)

def product_details(request, category_pk, product_pk):
    single_product = get_object_or_404(Product, category__pk=category_pk, pk=product_pk)
    
    context = {
        'single_product': single_product
    }
    return render(request, 'store/product_detail.html', context)

def store(request, category_pk=None):
    categories = None
    products = Product.objects.filter(is_available=True)

    if category_pk:
        categories = get_object_or_404(Category, pk=category_pk)
        products = products.filter(category=categories)

    product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/shop.html', context)



