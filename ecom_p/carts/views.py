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




@login_required
def add_to_cart(request, product_id):
    print(product_id)
    product = Product.objects.get(id=product_id)
    variant_id = request.POST.get('variant')  # Fetch the selected variant_id

    user = request.user

    try:
        variant = Variant.objects.get(id=variant_id)  # Get the corresponding Variant instance
    except Variant.DoesNotExist:
        return JsonResponse({'error': 'Variant not found'}, status=404)

    # Get or create the user's cart
    cart, _ = Cart.objects.get_or_create(user=user)

    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(
        user=user, product=product, variant=variant, cart=cart
    )

    # If the item is already in the cart, update the quantity and cart price
    if not created:
        cart_item.quantity += 1  # Increment the quantity
        cart_item.cart_price = product.product_price * cart_item.quantity  # Update the cart price
        cart_item.save()
    else:
        cart_item.quantity = 1  # Set initial quantity to 1 for a new cart item
        cart_item.cart_price = product.product_price  # Set initial cart price
        cart_item.save()

    return redirect('cart')





    

            

# def remove_cart(request, product_id, cart_item_id):
#     product = get_object_or_404(Product, id=product_id)
#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)  # <-- Corrected field name
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)  # <-- Corrected field name

#         if cart_item.quantity > 1:  # <-- Corrected field name
#             cart_item.quantity -= 1  # <-- Corrected field name
#             cart_item.save()
#         else:
#             cart_item.delete()
#     except:
#         pass        
#     return redirect('cart')

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