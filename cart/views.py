from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,ProductImage,ProductSize
from cart.models import Cart,CartItems
from account.models import CustomUser,UserProfile
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from cart.models import Wishlist
from django.contrib import messages

# Create your views here.
def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItems.objects.filter(cart=cart)
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
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
    product=ProductSize.objects.get(id=product_id)
    if request.method=='POST':
        size=request.POST.get('size')
         
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(cart_id=_cart_id(request),user=request.user)
    cart.save()
    try:
        cart_item=CartItems.objects.get(product=product,cart=cart)
        if cart_item.quantity<product.stock:
            cart_item.quantity += 1
        else:
            cart_item.quantity=product.stock
            messages.error(request,'Product has reached its maximum stock')
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
    product=get_object_or_404(ProductSize,id=product_id)
    cart_item=CartItems.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

def remove_cart_items(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(ProductSize,id=product_id)
    cart_item=CartItems.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')



def wishlist(request):
    wishlist=Wishlist.objects.filter(user=request.user)
    products=ProductSize.objects.filter(id__in=wishlist.values('product'))
    product_image=[]
    for product in products:
        product_images=ProductImage.objects.filter(product_size=product).first()
        if product_images:
            product_image.append(product_images)
    
    
    context={
        'wishlist':wishlist,
        'product_image':product_image,
    }
    return render(request,'user/wishlist.html',context)


def add_wishlist(request,id):
    user=request.user
    product=get_object_or_404(ProductSize,id=id)
    wishlist=Wishlist.objects.filter(user=user)
    if not wishlist.filter(user=user,product=product).exists():
        Wishlist.objects.create(user=user,product=product)
        messages.success(request,'Product added to your wishlist')
        return redirect('wishlist')

    return redirect('product_details',category_slug=product.product.category.slug,product_slug=product.slug)

def remove_wishlist(request,id):
    user=request.user
    product=get_object_or_404(ProductSize,id=id)
    wishlist=Wishlist.objects.filter(user=user,product=product)
    wishlist.delete()
    messages.info(request,'Product removed from wishlist')
    return redirect ('wishlist')
