from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from store.models import Product , Variant, Wishlist
from .models import Cart,CartItem,Coupon
from django.contrib import messages
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from user.models import Profile
from decimal import Decimal
from django.db.models import Q
from orders.models import Order
from django.db.models import F
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
                cart_item.is_active = False
                cart_item.save()
                total = total-(cart_item.product.product_price * cart_item.quantity)
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
    # request.session['wishlist_variant_id'] = variant_id
    # return redirect('add_to_cart', product_id=product_id)
    variant = Variant.objects.get(id=variant_id)
    cart = CartItem.objects.create
    current_user = request.user
    product = Product.objects.get(id=product_id)


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
            messages.success(request,"The item is already in your cart, and the quantity of the cart item has been increased")

            if request.user.is_authenticated:
                wishlist_item = Wishlist.objects.get(variant = variant_id, user=request.user)
                wishlist_item.delete()


        except CartItem.DoesNotExist:
            cart_item =CartItem.objects.create(product =product,quantity =+ 1,user=current_user,variant=variant,cart=cart, cart_price=product.product_price)
            cart_item.save()

            if request.user.is_authenticated:
                wishlist_item = Wishlist.objects.get(variant = variant_id, user=request.user)
                wishlist_item.delete()


            messages.success(request,"The item has been successfully added to your cart")
        return redirect("wishlist") 
    
    return redirect("wishlist")
    
    

    

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
    

    if action == 'Add to Cart' or action == None:
        print("add to carttttttttttt")
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
                # cart_item.quantity += 1  
                cart_item.quantity = F('quantity') + 1  # Increase the quantity by 1
                cart_item.cart_price = product.product_price*cart_item.quantity  
                print(cart_item.cart_price,"9999999999999999")
                cart_item.save()
                messages.success(request,"The item is already in your cart, and the quantity of the cart item has been increased")

            except CartItem.DoesNotExist:
                cart_item =CartItem.objects.create(product =product,quantity =+ 1,user=current_user,variant=variant,cart=cart, cart_price=product.product_price)
                cart_item.save()

                messages.success(request,"The item has been successfully added to your cart")
            return redirect("product_details", product_id) 
        else:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request)) 
            except Cart.DoesNotExist:
                cart = Cart.objects.create( cart_id = _cart_id(request))
            cart.save()
            try:
                cart_item = CartItem.objects.get(product=product, cart = cart, variant=variant)
                cart_item.quantity += 1 
                cart_item.cart_price = product.product_price*cart_item.quantity         
                cart_item.save()
                messages.success(request,"The item is already in your cart, and the quantity of the cart item has been increased")
            except CartItem.DoesNotExist:
                cart_item =CartItem.objects.create(product =product,quantity = cart_quantity+1,cart =cart ,variant=variant, cart_price=product.product_price)
                cart_item.save()
                messages.success(request,"The item has been successfully added to your cart")
        return redirect("product_details", product_id)
    elif action == 'Add to Wishlist':
        print("add to wishlist")
        return redirect('add_to_wishlist', variant_id=variant.id)
    else:
        return redirect('product_details', productid=product_id)
  


# def update_quantity(request):
#     print(update_quantity,"setttttttttttttttt")
#     if request.method == 'POST':
#         item_id = request.POST.get('item_id')
#         print(item_id,"itemmmmmmmmmmmmmm")
#         change = int(request.POST.get('change'))
#         print(change,"changeeeeeeeeeeeee")
#         cart_item = CartItem.objects.get(id=item_id)
#         product = cart_item.product
#         variant = cart_item.variant
#         # cart_item.quantity += change

        

#         if change == -1:
#             if cart_item.quantity > 1:
#                 cart_item.quantity += change
#                 cart_item.cart_price -= product.product_price
#             else:
#                 pass

            
#         elif change == 1:
#             if cart_item.variant.variant_stock > cart_item.quantity:
#                 cart_item.quantity += change
#                 cart_item.cart_price += product.product_price
#             else:
#                 pass
#         else:
#             pass
#         cart_item.save()

#         updated_price = cart_item.cart_price
#         updated_quantity = cart_item.quantity

#         tax = (2*updated_price)/100
#         grand_total = updated_price + tax
#         print(grand_total,"granddddddddd")
#         return JsonResponse({'updated_quantity': updated_quantity, 'updated_price': updated_price, 'tax':tax, 'grand_total':grand_total})
#     else:
#         return JsonResponse({'error': 'Invalid request method.'})
                



def update_quantity(request, updated_price=0,new_updated_price=0):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        print(item_id,"itemmmmmmmmmmmmmm")
        change = int(request.POST.get('change'))
        print(change,"changeeeeeeeeeeeee")
        cart_item = CartItem.objects.get(id=item_id)
        product = cart_item.product
        variant = cart_item.variant
        # cart_item.quantity += change

        # new_updated_price += cart_item.cart_price
        # print(new_updated_price,"new quantityyyyyyyyyyyy")



        if change == -1:
            if cart_item.quantity > 1:
                cart_item.quantity += change
                cart_item.cart_price -= product.product_price
            else:
                pass

            
        elif change == 1:
            if cart_item.variant.variant_stock > cart_item.quantity:
                cart_item.quantity += change
                cart_item.cart_price += product.product_price
            else:
                pass
        else:
            pass
        cart_item.save()

        new_price = CartItem.objects.get(id=item_id)
        new_updated_price = new_price.cart_price


        current_user = request.user
        if current_user.is_authenticated:
            cart = Cart.objects.get(cart_id = current_user, user = current_user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request)) 

        cart_items = CartItem.objects.filter(cart = cart)
        
        for cart in cart_items:
            updated_price += cart.cart_price

        # updated_price = cart_item.cart_price
        updated_quantity = cart_item.quantity

        tax = (2*updated_price)/100
        grand_total = updated_price + tax
        print(grand_total,"granddddddddddd")
        return JsonResponse({'updated_quantity': updated_quantity, 'updated_price': new_updated_price, 'tax':tax, 'grand_total':grand_total})
    else:
        return JsonResponse({'error': 'Invalid request method.'})
                

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
def checkout(request,total=0, quantity=0, coupon_amount=0, coupon_id = 0, cart_item=None):
    address_count = Profile.objects.filter(user=request.user).count()
        
    if address_count<1:
        return redirect('change_address')
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
                total += (Decimal(cart_item.product.product_price) * cart_item.quantity)
                quantity += cart_item.quantity

                if cart_item.variant.variant_stock == 0:
                    total -= Decimal(cart_item.product.product_price)

            # tax = (2*total)/100
            tax = (Decimal('0.02') * total)
            grand_total = total + tax    
        except ObjectDoesNotExist:
            pass # just ignore
        try:
            address = Profile.objects.get(user=request.user, set_default=True)
        except:
            address = Profile.objects.get(user=request.user)
            address.set_default = True
            address.save()
        total_address = Profile.objects.filter(user=request.user).count()

        if request.method == 'POST':
            print("haiiiiiiiiiiiii")
            couponcode = request.POST.get('CouponCode')
            print(couponcode, "its coupon code")

            try:
                exist_coupon = Coupon.objects.get(code=couponcode)
                print(exist_coupon,"exitttttttttttt")
                
                # Check if the coupon is active
                if not exist_coupon.is_active:
                    messages.info(request, "This coupon is not currently active.")
                
                # Check if the coupon has expired
                current_date = datetime.now().date()
                if current_date < exist_coupon.start_date:
                    messages.info(request, "This coupon is not yet valid.")
                elif current_date > exist_coupon.end_date:
                    messages.info(request, "This coupon has expired.")
                
                if grand_total < exist_coupon.min_price:
                    messages.info(request,"Parchase more for applay this coupon.")
                elif grand_total > exist_coupon.max_price:
                    messages.info(request,"This coupon is not applaied for the price range")
                else:
                    grand_total = grand_total - exist_coupon.discount_price
                    coupon_amount = exist_coupon.discount_price
                    messages.success(request,"coupon applied successfulley")
                    print(coupon_amount,"settttttttttttttt")
                    coupon_id = exist_coupon.id
                    print(coupon_id,"carttttttttttcouponid")

            
            except Coupon.DoesNotExist:
                messages.info(request, "The entered coupon code is not valid")
        else:
            pass



        coupons = Coupon.objects.filter(
            Q(min_price__lt=grand_total) & Q(max_price__gt=grand_total)
        )

        orders = Order.objects.filter(user=request.user)
        unused_coupons = []

        for coupon in coupons:
            coupon_used = False
            for order in orders:
                if order.coupon == coupon:
                    coupon_used = True
                    break  # No need to check other orders if coupon is found in one
            if not coupon_used:
                unused_coupons.append(coupon)

        if total == 0:
            return redirect('store')
        context = {
            'total' : total,
            'quantity' : quantity,
            'cart_items' : cart_items,
            'tax':tax,
            'grand_total':grand_total,
            'address':address,
            'total_address' : total_address,
            'coupon_amount' : coupon_amount,
            'coupon_id': coupon_id,
            'coupons' : unused_coupons,
        }
        print(context,"''''''''''''''''''''")
    return render(request, 'orders/checkout.html', context)


