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



# def payment(request):
#     return render(request, 'payment.html')

def about(request):
    return render(request,"about.html")





def banner(request):
    banners = Banner.objects.all().filter(is_available=True)
    context={
        'banners':banners
    }
    return render(request,'layouts/index.html',context)



# def shop(request):
#     products = Product.objects.filter(is_available=True)
#     context = {
#         'products': products,
#     }
#     return render(request, 'store/shop.html', context)


def product_details(request, productid):
    single_product = Product.objects.get(id=productid)
    variation = Variant.objects.filter(product=productid)
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> PG-1

    wishlist = Wishlist.objects.all()
    print(variation,"9999909990990990909")
    print(single_product.id,"0000000000000000000")
  # Create a list of variant IDs in the wishlist
    wishlist_variant_ids = [item.variant.id for item in wishlist]
    

<<<<<<< HEAD
=======
    print(variation,"9999909990990990909")
    print(single_product.id,"0000000000000000000")
>>>>>>> parent of f08f8d3 (modified profile,cart,wishlist,checkout,payment)
=======
>>>>>>> PG-1
    context = {
        'single_product': single_product,
        'variation':variation,
        # 'in_cart':in_cart
    }
    return render(request, 'store/product_detail.html', context)

<<<<<<< HEAD
=======



>>>>>>> PG-1
def store(request):
    
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.filter(is_available=True)
    paginator = Paginator(products, 2)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    print(products)
    context = {
        'products': paged_products,
        'categories':categories,
    }
    return render(request, 'store/shop.html', context)

def categories(request, categoryid):
    products = Product.objects.filter(category=categoryid)
    categories = Category.objects.filter(is_available=True)
    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    print(products)
    context = {
        'products':paged_products,
        'categories':categories,

    }
    return render(request, 'store/shop.html',context)


@require_GET
def get_variant_details(request):
    
    variant_id = request.GET.get('variantId')
    try:
<<<<<<< HEAD
        variant = Variant.objects.select_related('product').prefetch_related('variant_image').get(id=variant_id)
=======
        print('yes inside')
        variant = Variant.objects.select_related('product').get(id=variant_id)
        stock_status = variant.variant_stock > 0 
>>>>>>> PG-1
        variant_data = {
            'variant_image': variant.images.first().variant_image.url,
            'variant_price': variant.price,
            'variant_name': variant.product.product_name,
            'variant_stock': variant.variant_stock,
            'variant_status': variant.is_available,
<<<<<<< HEAD
=======
            'stock_status' : stock_status,
            
>>>>>>> PG-1
        }
        return JsonResponse(variant_data)
    except Variant.DoesNotExist:
        return JsonResponse({'error': 'Variant not found'}, status=404)


<<<<<<< HEAD
=======
def get_variant_stock_status(request):
    if request.method == 'GET' and request.is_ajax():
        variant_id = request.GET.get('variantId')
        variant = get_object_or_404(Variant, id=variant_id)  # Replace with your model's field names
        print(variant,"vvvvvvvvvvvv")
        stock_status = variant.variant_stock > 0  # Adjust this condition based on your model's stock field
        return JsonResponse({'stock_status': stock_status})
    return JsonResponse({}, status=400)



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
>>>>>>> PG-1
