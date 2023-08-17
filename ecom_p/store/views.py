from django.shortcuts import render,get_object_or_404
from store.models import Product,Banner,Variant
from category.models import Category
from django.urls import reverse
from django.http import Http404, HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_GET

# from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.

def home(request):
    products = Product.objects.filter(new_arrival=True)
    print(products)
    context = {
        'products':products
    }
    
    return render(request,'layouts/index.html',context)

def contact(request):
    return render(request,'contact.html')

def checkout(request):
    return render(request,'checkout.html')

# def payment(request):
#     return render(request, 'payment.html')

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
        'products': products,
    }
    return render(request, 'store/shop.html', context)


def product_details(request, productid):
    single_product = Product.objects.get(id=productid)
    variation = Variant.objects.filter(product=productid)
    print(variation,"9999909990990990909")
    print(single_product.id,"0000000000000000000")
    context = {
        'single_product': single_product,
        'variation':variation,
        # 'in_cart':in_cart
    }
    return render(request, 'store/product_detail.html', context)

def store(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.filter(is_available=True)
    context = {
        'products': products,
        'categories':categories,
    }
    return render(request, 'store/shop.html', context)

def categories(request, categoryid):
    products = Product.objects.filter(category=categoryid)
    categories = Category.objects.filter(is_available=True)

    print(products)
    context = {
        'products':products,
        'categories':categories,

    }
    return render(request, 'store/shop.html',context)


@require_GET
def get_variant_details(request):
    
    variant_id = request.GET.get('variantId')
    print(variant_id,"hrlooooooooooooooooo")
    try:
        variant = Variant.objects.select_related('product').prefetch_related('variant_image').get(id=variant_id)
        variant_data = {
            'variant_image': variant.images.first().variant_image.url,
            'variant_price': variant.price,
            'variant_name': variant.product.product_name,
            'variant_stock': variant.variant_stock,
            'variant_status': variant.is_available,
            # Include other variant details as needed
        }
        return JsonResponse(variant_data)
    except Variant.DoesNotExist:
        return JsonResponse({'error': 'Variant not found'}, status=404)


