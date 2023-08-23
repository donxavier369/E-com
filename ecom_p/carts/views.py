from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from store.models import Product , Variant, Wishlist
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
    variants = Variant.objects.all()
    list = []
    for variant in variants:
        if variant.variant_stock < 1:
            list.append(variant.id)
    print(list,"out of stock")
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
            
            if cart_item.variant.variant_stock == 0:
                total = total-cart_item.product.product_price
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
        'list':list,
    }         
    return render(request, 'store/cart.html', context)

# views.py

def wishlist_to_cart(request, product_id, variant_id):
    print(variant_id,"varianttttttttttttt in wishlis")
    request.session['wishlist_variant_id'] = variant_id
    return redirect('add_to_cart', product_id=product_id)

    

def add_to_cart(request,product_id,variant=0):
    print(product_id,"product_idddddddddddddd")
    variant_id_from_session = request.session.get('wishlist_variant_id')
    product = Product.objects.get(id=product_id)
    variant_id = request.POST.get('variant')  
    # quantity = int(request.POST.get('quantity'))  
    action = request.POST.get('action')
    current_user = request.user
    if variant_id:
        try:
            variant = Variant.objects.get(id=variant_id)
        except Variant.DoesNotExist:
            pass
    elif variant_id_from_session:
        try:
            variant = Variant.objects.get(id=variant_id_from_session)
        except Variant.DoesNotExist:
            pass
    print(variant,"variant in cartttttttttttttttt")
    

    if action == 'add to cart' or action == None:
        if action == None:
            wishlist = Wishlist.objects.get(variant=variant)
            wishlist.delete()
        print("add_to_cart")
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
                cart_item.cart_price = product.product_price*cart_item.quantity  
                print(cart_item.cart_price,"9999999999999999")
                cart_item.save()
            except CartItem.DoesNotExist:
                cart_item =CartItem.objects.create(product =product,quantity =+ 1,user=current_user,variant=variant,cart=cart, cart_price=product.product_price)
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
                cart_item.cart_price = product.product_price*cart_item.quantity         
                cart_item.save()
            except CartItem.DoesNotExist:
                cart_item =CartItem.objects.create(product =product,quantity = cart_quantity+1,cart =cart ,variant=variant)
                cart_item.save()
        return redirect('cart')
    elif action == 'add to wishlist':
        print("add to wishlist")
        return redirect('add_to_wishlist', variant_id=variant.id)
    else:
        return redirect('product_details', productid=product_id)
        
# def update_cart_item(request, id):
#     user=request.user
#     cart_item = get_object_or_404(CartItem, id=id)
#     cart=Cart.objects.get(user=user)
#     if request.method == 'POST':
#         new_quantity = int(request.POST.get('quantity', 0))
#         if new_quantity >= 0:
#             cart_item.quantity = new_quantity
#             cart_item.save()

#     # Prepare the data to be sent back in the AJAX response
#     data = {
#         'subtotal': cart_item.get_subtotal(),
#         'price':cart.get_total_price(),
#         'quantity':cart.get_total_quantity(),
#     }
#         # Return the updated data as a JSON response
#     return JsonResponse(data)
   
# def update_cart_item(request, id):
#     print("update_cart_item_quantity",id)
#     user=request.user
#     cart_item = get_object_or_404(CartItem, id=id)
#     cart=Cart.objects.get(user=user)
#     if request.method == 'POST':
#         new_quantity = int(request.POST.get('quantity', 0))
#         if new_quantity >= 0:
#             cart_item.quantity = new_quantity
#             cart_item.save()

#     # Prepare the data to be sent back in the AJAX response
#     data = {
#         'subtotal': cart_item.get_subtotal(),
#         'price':cart.get_total_price(),
#         'quantity':cart.get_total_quantity(),
#     }
#         # Return the updated data as a JSON response
#     return JsonResponse(data)



def update_cart_item(request,item_id):
    if request.method == 'POST' and request.is_ajax():
        # item_id = request.POST.get('id')
        new_quantity = int(request.POST.get('quantity', 0))
        print(item_id,"itemmmmmmmmmm")
        cart_item = CartItem.objects.get(id=item_id)
        # Perform necessary logic to update the cart item's quantity in the database
        # Replace this with your own logic to update the cart item and calculate the new subtotal
        
        # For demonstration purposes, let's assume the updated subtotal is calculated as follows:
        updated_subtotal = new_quantity * 10.0  # Assuming each item costs $10

        # Simulate a response with updated values
        response = {
            'subtotal': updated_subtotal,
            'price': '123.45',  # Replace with the actual total price after updating the cart
            'quantity': '5'     # Replace with the actual total quantity after updating the cart
        }

        return JsonResponse(response)
    else:
        return JsonResponse({'error': 'Invalid request'})

                


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

                if cart_item.variant.variant_stock == 0:
                    total = total-cart_item.product.product_price

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
            'coupon_amount' : total_address,
        } 
    return render(request, 'orders/checkout.html', context)


