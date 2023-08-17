from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,ProductImage,ProductSize
from cart.models import Cart,CartItems
from account.models import CustomUser,UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
# Create your views here.
def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItems.objects.filter(cart=cart)
        for cart_item in cart_items:
            total+=(cart_item.product.product_size.price * cart_item.quantity)
            quantity+=cart_item.quantity
        tax=(5*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist:
        pass
    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request,'user/cart.html',context)

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
    size=request.POST.get('size')
    
    product=ProductImage.objects.get(id=product_id)     
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cart_id(request),user=request.user)
    cart.save()

    try:
        cart_item=CartItems.objects.get(product=product,cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItems.DoesNotExist:
        cart_item=CartItems.objects.create(product=product,quantity=1,cart=cart)
        cart_item.save()
    return redirect('cart')

    # product=get_object_or_404(ProductSize, id=product_id)
    # cart=Cart.objects.get_or_create(user=request.user)
    # cart_item=CartItems.objects.get_or_create(cart=cart,product=product)
    # cart_item.quantity+=1
    # cart_item.save()
    # cart=CartItems.objects.all()
    # return redirect('cart')


def remove_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(ProductImage,id=product_id)
    cart_item=CartItems.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_items(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(ProductImage,id=product_id)
    cart_item=CartItems.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')

# def checkout(request):
#     user=request.user
#     address=UserProfile.objects.filter(user=user)
#     print(address)
#     cart_items=CartItems.objects.filter(cart__user=user)
#     context={
#         'user':user,
#         'address':address,
#         'cart_items':cart_items,
#     }
#     return render(request,'user/checkout.html',context)

