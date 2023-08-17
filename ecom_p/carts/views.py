from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from store.models import Product , Variant
from .models import Cart,CartItem

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from user.models import Profile
# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart    



def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:   
            cart = Cart.objects.get(cart_id=_cart_id(request))
            print(cart,'222222222222222222')                             
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            print(cart_items,"1111111111111111111")
        for cart_item in cart_items:
            total += (cart_item.product.product_price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total)/100
        grand_total = total + tax    
    except ObjectDoesNotExist:
        pass # just ignore
    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }         
    return render(request, 'store/cart.html', context)


def add_to_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    variant_id = request.POST.get('variant')  
    # quantity = int(request.POST.get('quantity'))  
    current_user = request.user
    variant = Variant.objects.get(id = variant_id)
    try:
        get_product = CartItem.objects.get(product=product)
        cart_quantity = get_product.quantity
    except:
        cart_quantity = 0

    if current_user.is_authenticated:
        try:
            cart = Cart.objects.get(cart_id = current_user, user = current_user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = current_user, user = current_user)
        try:
            cart_item = CartItem.objects.get(product=product, user=current_user, variant=variant, cart = cart)
            cart_item.quantity += 1  
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item =CartItem.objects.create(product =product,quantity = cart_quantity+1,user=current_user,variant=variant,cart=cart)
            cart_item.save()
        return redirect('cart')  
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) 
        except Cart.DoesNotExist:
            cart = Cart.objects.create( cart_id = _cart_id(request))
        cart.save()
        try:
            cart_item = CartItem.objects.get(product=product, cart = cart,variant=variant)
            cart_item.quantity += 1           
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item =CartItem.objects.create(product =product,quantity = cart_quantity+1,cart =cart ,variant=variant)
            cart_item.save()
    return redirect('cart')
   

def update_cart_item_quantity(request, cart_item_id, action):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)

        if action == 'increase':
            if cart_item.variant.variant_stock > 0 and cart_item.variant.variant_stock > cart_item.quantity:
                cart_item.quantity += 1
                cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                # if cart_item.quantity == 0:
                #     cart_item.delete()
            else:
                pass
        else:
            pass
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')
                

def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)

    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')





@login_required(login_url='handlelogin')
def checkout(request,total=0, quantity=0, cart_item=None):
    address_count = Profile.objects.filter(user=request.user).count()
        
    if address_count<1:
        return redirect('add_address')
    else:
        try:
            tax = 0
            grand_total = 0
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            else:   
                cart = Cart.objects.get(cart_id=_cart_id(request))
                print(cart,'222222222222222222')
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
                print(cart_items,"1111111111111111111")
            for cart_item in cart_items:
                total += (cart_item.product.product_price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2*total)/100
            grand_total = total + tax    
        except ObjectDoesNotExist:
            pass # just ignore

        address = Profile.objects.get(user=request.user, set_default=True)
        total_address = Profile.objects.filter(user=request.user).count()


        context = {
            'total' : total,
            'quantity' : quantity,
            'cart_items' : cart_items,
            'tax':tax,
            'grand_total':grand_total,
            'address':address,
            'total_address' : total_address,
        } 
    return render(request, 'orders/checkout.html', context)










