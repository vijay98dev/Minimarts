from django.shortcuts import render,redirect,get_object_or_404
from cart.models import Cart,CartItems
from account.models import UserProfile
from orders.models import Order,OrderProduct
import razorpay
from django.conf import settings

# Create your views here.


def checkout(request,total=0,quantity=0):
    user=request.user

#If the cart count is less than or equal to 0 , then redirect to store 

    cart_items=CartItems.objects.filter(cart__user=user)
    print(cart_items)
    cart_count=cart_items.count()
    if cart_count<=0:
        return redirect('store')
    
    grand_total=0
    tax=0
    for cart_item in cart_items:
        total+=(cart_item.product.price * cart_item.quantity)
        quantity+=cart_item.quantity
    tax=(5*total)/100
    grand_total = total+tax
    address=UserProfile.objects.filter(user=user)
    # client=razorpay.Client(auth=(settings.razor_pay_key_id,settings.key_secret))
    # payment=client.order.create({'amount'})
    context={
        'address':address,
        'cart_item':cart_items,
        'cart_count':cart_count,
        'total':total,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request,'user/checkout.html',context)

def payment_confirmation(request):
    return render(request,'user/payment-confirmation.html')


def confirmation(request):
    return render (request,'user/confirmation.html')

# def place_order(request):
    # if request.method == 'POST':
    #     address_id=request.POST.get('address')
    #     payment_method=request.POST.get('pay-method')
    #     print(payment_method)
    # cart=get_object_or_404(Cart,user=request.user)
    # address=get_object_or_404(UserProfile,id=address_id)
    # # price1=cart.total_price()
    # # payment_amount1=cart.total()
    # # shipping_charge=cart.shipping_charge()
    # order=Order.objects.create(
    #     user=request.user,
    #     address=address,
    #     payment_method=payment_method,
    #     # price=price1,
    #     # offer_price=payment_amount1,
    #     # payment_amount=payment_amount1,
    #     # shipping_charge=shipping_charge,
    #     )
    # for cart_item in CartItems.objects.all():
    #     OrderProduct.objects.create(
    #         order=order,
    #         payment=payment_method,
    #         user=request.user,
    #         product=cart_item.product,
    #         product=cart_item.strap,
    #         quantity=cart_item.quantity,
    #         )
    # cart.delete()
    # context={
    #     "address":address,
    #     'payment_method':payment_method,
    #     'order_id':order.order_id,
    #     }
    # return render (request,'user/confirmation.html')
