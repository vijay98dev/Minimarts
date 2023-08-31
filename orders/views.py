from django.shortcuts import render,redirect,get_object_or_404
from cart.models import Cart,CartItems
from account.models import UserProfile
from orders.models import Order,OrderProduct,Payment
import razorpay
import os
from django.contrib import messages
import datetime
from dotenv import load_dotenv


# Create your views here.


# def place_order(request):
#     order=Order.objects.get(user=request.user,is_paid=False)
#     if request.method =="POST":
#         payment_method=request.POST.get('pay-method')
    
#     context={
#         }
#     return render (request,'user/payment-confirmation.html',context)




def checkout(request,total=0,quantity=0):
    user=request.user

#If the cart count is less than or equal to 0 , then redirect to store 

    cart_items=CartItems.objects.filter(cart__user=user)
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
    # client=razorpay.Client(auth=(os.environ['razor_pay_key_id'],os.environ['key_secret'])
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


def confirmation(request):
    return render (request,'user/confirmation.html')

def create_order(request,total=0):
    user=request.user
    address_id=None
    order=None
    payment=None
    cart_items=CartItems.objects.filter(cart__user=user)
    grand_total=0
    tax=0
    for cart_item in cart_items:
        total+=(cart_item.product.price * cart_item.quantity)
    tax=(5*total)/100
    grand_total = total+tax
    if request.method == 'POST':
        if 'checkout_submit' in request.POST:
            address_id=request.POST.get('address')
            try:
                address=UserProfile.objects.get(id=address_id)
            except UserProfile.DoesNotExist:
                if not address_id:
                    messages.info(request,'Please select an address ')
                    return redirect('checkout')
            order=Order.objects.create(user=user,address=address,order_total=grand_total)
            order.save()
            #generate order number

            yr=int(datetime.date.today().strftime('%Y'))
            dt=int(datetime.date.today().strftime('%d'))
            mt=int(datetime.date.today().strftime('%m'))
            d=datetime.date(yr,mt,dt)
            current_date=d.strftime("%Y%m%d")
            order_number=current_date+str(order.id)
            order.order_number=order_number
            order.save()
            
        elif 'payment_submit' in request.POST:
            payment_method=request.POST.get('pay-method')
            print(payment_method)
            if payment_method=='cod':
                if order is None:
                    messages.info(request,'Please complete checkout')
                    return redirect ('checkout')
                payment=Payment.objects.create(user=user,payment_method=payment_method)
                payment.save()
                if payment.status == 'Completed':
                    payment.amount_paid=grand_total
                    payment.save()
                    print(payment.id)
                order.is_paid=True
                order.payment=payment.id
                order.save()
                return redirect('confirmation')
            elif payment_method=='razorpay':
                load_dotenv()
                client=razorpay.Client(auth=(os.getenv('RAZOR_PAY_KEY_ID'),os.getenv('KEY_SECRET')))
                payment=client.order.create({'amount':order.order_total*100 , 'currency':'INR', 'payment_capture':1})
                print(payment)

                # payment=Payment(user=user,)
    # cart=Cart.objects.get(user=request.user)
    # cart_items=CartItems.objects.filter(cart=cart)
    
    # address=get_object_or_404(UserProfile,id=address_id)
    context={
        'order':order,
        'payment':payment
    }
    return render(request,'user/payment-confirmation.html',context)

def my_order(request):
    user=request.user
    
    context={

    }
    return render(request,'user/my-order.html',context)