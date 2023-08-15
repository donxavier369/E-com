from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.db.models import Q
from django.urls import reverse
from user.models import CustomUser
from django.contrib.auth import authenticate,login,logout
from store.models import Product , Variant
from category.models import  Category, Brand
from django.shortcuts import get_object_or_404
from orders.models import Order
# from store.models import Variation
# Create your views here.


def manageuser(request):
    if request.user.is_authenticated and request.path != reverse('manageuser'):
        return redirect('manageuser')

    data = CustomUser.objects.filter(is_superuser=False)  # Define data here

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

def admin_login(request):
    if request.user.is_authenticated and  request.user.is_superuser==True:
        return redirect('admin_page')
    if request.method=="POST":
        email=request.POST.get("email")
        pass1=request.POST.get("pass1")
        myuser = authenticate(email=email,password=pass1)
        if myuser is not None:
            if myuser.is_superuser:
                login(request,myuser)
                messages.success(request,"Login Success!")
                return redirect('admin_page')
            elif myuser is not myuser.is_superuser:
                messages.error(request,"You are not an Admin")
                return redirect('admin_login')
        else:
            messages.error(request,"Invalid Credentials")

    return render(request,"adm/admin_login.html")             
            
def admin_logout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('admin_login')


def admin_page(request):
    if request.user.is_authenticated and request.user.is_superuser==True:
        return render(request,"Admin/adminindex.html")
    else:
        return render(request, "adm/admin_login.html")

# product management

def product(request):
        products = Product.objects.all()
        categories = Category.objects.filter(is_available=True)
        product_count = products.count()
        brands = Brand.objects.all()
        variant = Variant.objects.all()
        
        context = {
            "products" : products,
            "product_count" : product_count,
            "categories" : categories,
            "brands" : brands,
            "variant":variant,
           
        }
        return render(request, "Admin/AdminFunctions/product.html",context)



def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        category_id = request.POST.get('product_category')
        new_arrival = request.POST.get('product_new_arrival')
        brand_id = request.POST.get('product_brand')
        product_description = request.POST.get('product_description')
        product_image = request.FILES.get('product_image')
        product_price = request.POST.get('product_price')
        category = get_object_or_404(Category, id=category_id)
        brand = get_object_or_404(Brand, id=brand_id)

        product = Product(
            product_name=product_name,
            category=category,
            new_arrival=(new_arrival == '1'),  # Convert to boolean
            brand=brand,
            description=product_description,
            product_price = product_price,
        
            images=product_image
        )
        product.save()

        return redirect('product')  # Replace 'product' with the name of the view that displays the list of products
    categories = Category.objects.all()
    brands = Brand.objects.all()
    return render(request, 'Admin/AdminFunctions/product.html', {'categories': categories, 'brands': brands})

    
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        brand_id = request.POST.get('brand')  # Use 'brand' instead of 'product_brand'
        category_id = request.POST.get('category')  # Use 'category' instead of 'product_category'
        product_price = request.POST.get('product_mrp')
        product_stock = request.POST.get('product_stock')
        product_description = request.POST.get('product_description')
        product_price = request.POST.get('product_description')

        # Retrieve the updated 'images' field value
        product_thumbnail = request.FILES.get('product_images')
        print(product_thumbnail,"thumbbbbbbbbbbbbbbbbbb")

        # Update other product details
        product.product_name = product_name
        product.brand = get_object_or_404(Brand, id=brand_id)
        product.category = get_object_or_404(Category, id=category_id)
        product.price = product_price
        product.stock = product_stock
        product.description = product_description


        # Only update 'images' if a new file was provided
        if product_thumbnail:
            product.images = product_thumbnail

        # Save the updated product
        product.save()

        return redirect('product')

    return render(request, 'admin/product_list.html', {'product': product})
def product_add(request):

    return render(request,"Admin/AdminFunctions/product.html")

def product_block(request,id):
    block = Product.objects.filter(id=id).update(is_available=False)
    return redirect("product")

def product_unblock(request,id):
    un_block = Product.objects.filter(id=id).update(is_available=True)
    return redirect("product")



#category management

def category(request):
    categories = Category.objects.all()
    return render(request,"Admin/AdminFunctions/category.html",{'categories': categories})

def category_block(request,id):
    block = Category.objects.filter(id=id).update(is_available = False)
    return redirect("category")

def category_unblock(request,id):
    un_block = Category.objects.filter(id=id).update(is_available = True)
    return redirect("category")


def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description')
        Is_available = request.POST.get('Is_available')
        productImage = request.FILES.get('productImage')
        category = Category.objects.create(
            category_name=category_name,
            description=category_description,
            cat_image=productImage,
            is_available=Is_available
        )
        return redirect('category')

    return render(request, "Admin/AdminFunctions/category.html")



def edit_category(request, id):
    category = get_object_or_404(Category,id=id)
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description')
        category_thumbnail = request.FILES.get('category_images')


        category.category_name = category_name
        category.description = category_description

        if category_thumbnail:
            category.cat_image = category_thumbnail

        category.save()

        return redirect('category')    

    return render(request,"Admin/AdminFunctions/category.html")


# order management

def manage_order(request):
    orders = Order.objects.all()
    statuses = Order.STATUS
    
    context = {
        'orders' : orders,
        'statuses' : statuses,
    }
    return render(request, "Admin/AdminFunctions/order.html",context)

def manage_orderstatus(request, id):
    order = get_object_or_404(Order,id=id)
    if request.method == 'POST':
        order_status = request.POST.get('status')
        order.status = order_status
        order.save()
        return redirect('manage_order')
    return render(request, "Admin/AdminFunctions/order.html")

# variant management

def variant(request,id):
    if request.method == 'POST':
        variant_colour = request.POST.get('variant_colour')
        variant_stock =request.POST.get('variant_stock')
        is_available = request.POST.get('variant_is_available')
        variant_image = request.FILES.get('variant_image')
        # variant_mrp = request.POST.get('variant_price')
        
       
        product = get_object_or_404(Product, id=id)
        variant = Variant.objects.create(  
             product = product,
            variant_colour = variant_colour,
            variant_stock = variant_stock,
            is_available = is_available,
            variant_image = variant_image,
            # variant_price = variant_mrp,
           
        )
        return redirect('product')

    return render(request,"Admin/AdminFunctions/product.html",{'variant':variant})


def variant_details(request,id):
    variant = get_object_or_404(Variant, id=id)
    if request.method == 'POST':
        variant_colour = request.POST.get('variant_colour')
        variant_stock =request.POST.get('variant_stock')
        is_available = request.POST.get('variant_is_available')
        variant_image = request.FILES.get('variant_image')
        # variant_mrp = request.POST.get('variant_price')

        variant.variant_colour = variant_colour
        variant.variant_stock = variant_stock
        variant.is_available = is_available
        # variant.variant_price = variant_mrp

        if variant_image:
            variant.variant_image = variant_image

        variant.save()
        return redirect('product')


    return render(request,"Admin/AdminFunctions/product.html")


def delete_variant(request, id):
    delete_variant = Variant.objects.filter(id=id)
    if delete_variant:
        delete_variant.delete()
        return redirect('product')
    return render(request,"Admin/AdminFunctions/product.html")

    
