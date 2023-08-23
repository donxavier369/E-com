from django.shortcuts import redirect, render,get_object_or_404
from store.models import Product,Banner,Variant,Wishlist
from category.models import Category
from django.urls import reverse
from django.http import Http404, HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
from decimal import Decimal

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
    wishlist = Wishlist.objects.all()
    print(variation,"9999909990990990909")
    print(single_product.id,"0000000000000000000")
  # Create a list of variant IDs in the wishlist
    wishlist_variant_ids = [item.variant.id for item in wishlist]
    
    context = {
        'single_product': single_product,
        'variation': variation,
        'wishlist_variant_ids': wishlist_variant_ids,
    }
    return render(request, 'store/product_detail.html', context)

from django.http import JsonResponse

def get_variant_stock_status(request):
    if request.method == 'GET':
        variant_id = request.GET.get('variantId')
        # Perform logic to get the stock status of the selected variant based on variant_id
        # For example, you might query your database for the stock status.
        variant = Variant.objects.get(id == variant_id)
        if variant.variant_stock < 1:
            variant_stock_status = False
        else:
            # Dummy logic for demonstration purpose
            variant_stock_status = True  # Assuming the variant is in stock

        response_data = {
            'stock_status': variant_stock_status,
        }
        return JsonResponse(response_data)
    else:
        # Handle other HTTP methods if needed
        pass


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
        print('yes inside')
        variant = Variant.objects.select_related('product').get(id=variant_id)
        variant_data = {
            'variant_image': variant.variant_image.url,
            'variant_name': variant.product.product_name,
            'variant_stock': variant.variant_stock, 
            'variant_status': variant.is_available,
            # Include other variant details as needed
        }
        print(variant_data['variant_stock'])

        return JsonResponse(variant_data)
    except Variant.DoesNotExist:
        return JsonResponse({'error': 'Variant not found'}, status=404)




def search(request):
    if request.method == "POST":
        keyword = request.POST.get('keyword')
        print(keyword,"keyyyyyyyyyey")
        products = Product.objects.filter(
            Q(description__icontains=keyword)
        )
        # paginator = Paginator(variant, 6)
        # page_number = request.GET.get('page')
        # variants = paginator.get_page(page_number)
        print(products,"vvvvvvvvvvvv")
        context = {
            "products": products,
            "keyword": keyword,
        }
        return render(request, "store/shop.html", context)
    return redirect('shop')



def filter_products_by_price(request):
    # Initialize the context dictionary
    context = {}

    if request.method == 'POST':
        # Get the price filter values from the submitted form
        price_min = Decimal(request.POST.get('price-min', 1000))
        price_max = Decimal(request.POST.get('price-max', 1000000))

        # Convert the Decimal values to float before storing them in the session
        request.session['selected_price_filter'] = {'min': float(price_min), 'max': float(price_max)}
        return redirect('filter_products_by_price')
    else:
        # If no form is submitted, check if there are stored price filter values in the session
        selected_price_filter = request.session.get('selected_price_filter')
        if selected_price_filter:
            # Convert the stored float values back to Decimal
            price_min = Decimal(selected_price_filter['min'])
            price_max = Decimal(selected_price_filter['max'])
        else:
            # If there are no stored price filter values, use default values
            price_min = Decimal(1000)
            price_max = Decimal(1000000)

    # Query the products within the specified price range and order them by some field (e.g., 'id')
    products = Product.objects.filter(product_price__gte=price_min, product_price__lte=price_max).order_by('id')

    # Pagination
    paginator = Paginator(products, 2)  # Set the number of products per page (e.g., 2 products per page)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    # Add the products and other relevant data to the context dictionary
    context['products'] = products
    context['product_count'] = paginator.count

    # Add the selected price filter to the context with default values
    context['selected_price_filter'] = {'min': price_min, 'max': price_max}

    # Add any other data you want to pass to the template
    # ...

    return render(request, 'store/shop.html', context)