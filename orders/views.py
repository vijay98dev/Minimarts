from django.shortcuts import render,redirect,get_object_or_404
from cart.models import Cart,CartItems,Coupons,UserCoupons
from account.models import UserProfile
from orders.models import Order,OrderProduct,Payment
from store.models import Product,ProductImage,ProductSize
from django.db.models import Max
import razorpay
import os
from django.contrib import messages
import datetime
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required


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
    discount=0
    for cart_item in cart_items:
        total+=cart_item.sub_total()
        quantity+=cart_item.quantity
        tax+=cart_item.tax()
        if cart_item.cart.coupon:
            discount=cart_item.discount_amount()
        grand_total+=cart_item.total_after_discount() 
    address=UserProfile.objects.filter(user=user)
    # client=razorpay.Client(auth=(os.environ['razor_pay_key_id'],os.environ['key_secret'])
    # payment=client.order.create({'amount'})
    context={
        'address':address,
        'cart_item':cart_items,
        'cart_count':cart_count,
        'total':total,
        'tax':tax,
        'discount':discount,
        'grand_total':grand_total
    }
    return render(request,'user/checkout.html',context)


def confirmation(request):
    order_id=request.GET.get('razorpay_order_id')
    payment_id=request.GET.get('razorpay_payment_id')
    signature=request.GET.get('razorpay_signature')
    payment=Payment.objects.get(razor_pay_order_id=order_id)
    payment.razor_pay_payment_id=payment_id
    payment.razor_pay_payment_signature=signature
    payment.save()
    order=Order.objects.get(id=payment.order_id)
    order.is_paid=True
    order.save()
    confirmed_payment=Payment.objects.get(razor_pay_order_id=order_id)
    order_items=OrderProduct.objects.filter(order_id=order.id)
    for items in order_items:
        items.payment_id=confirmed_payment.id
    return render (request,'user/confirmation.html')

@login_required
def create_order(request,total=0):
    user=request.user
    address_id=None
    order=None
    payment=None
    payment_method='razorpay'
    try:
        cart=Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return redirect('cart')
    cart_items=CartItems.objects.filter(cart__user=user)
    grand_total=0
    tax=0
    discount=0
    for cart_item in cart_items:
        total+=cart_item.sub_total()
        if cart.coupon:
            discount=cart_item.discount_amount()
        tax+=cart_item.tax()
    grand_total += total+tax-discount
        
    if request.method == 'POST':
        if 'checkout_submit' in request.POST:
            address_id=request.POST.get('address')
            try:
                address=UserProfile.objects.get(id=address_id)
            except UserProfile.DoesNotExist:
                if not address_id:
                    messages.info(request,'Please select an address ')
                    return redirect('checkout')
            order=Order.objects.create(user=user,address=address,order_total=grand_total,total=total,tax=tax,discount_price=discount)
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
            for items in CartItems.objects.all():
                product=items.product
                image=ProductImage.objects.get(product_size=product)
                order_items=OrderProduct.objects.create(order=order,payment=payment,user=user,product=product,product_image=image,quantity=items.quantity,product_price=items.product.price,sub_total=items.sub_total())
        # if 'payment_submit' in request.POST:
        #     print("else payment")
        #     payment_method=request.POST.get('pay-method')
        if 'payment_submit' in request.POST:
            payment_method='razorpay'
            order = Order.objects.filter(user=user).order_by('-created_at').first()
            
            payment_method=request.POST.get('pay-method')
            if payment_method=='cod':
                payment=Payment.objects.create(user=user,payment_method=payment_method,order=order)
                payment.save()
                payment=Payment.objects.get(order=order)

                return redirect('confirmation-cod' ,order.id)
                
            
    try:
        payment=Payment.objects.get(order=order)
        return redirect('confirmation')
    except Payment.DoesNotExist:
        load_dotenv()
        client=razorpay.Client(auth=(os.getenv('RAZOR_PAY_KEY_ID'),os.getenv('KEY_SECRET')))
        razorpay_payment=client.order.create({'amount':grand_total*100 , 'currency':'INR', 'payment_capture':1})
        print(razorpay_payment)
        payment=Payment.objects.create(user=user,payment_method='razorpay',amount_paid=grand_total,razor_pay_order_id=razorpay_payment['id'],order=order)
        payment.save()
        print(payment.id)
        # print('11111111111111')
        # if payment_method=='razorpay':
        #     print('1212121212121212121')
        #     load_dotenv()
        #     client=razorpay.Client(auth=(os.getenv('RAZOR_PAY_KEY_ID'),os.getenv('KEY_SECRET')))
        #     razorpay_payment=client.order.create({'amount':grand_total*100 , 'currency':'INR', 'payment_capture':1})
        #     print(razorpay_payment)
        #     payment=Payment.objects.create(user=user,payment_method='razorpay',amount_paid=grand_total,razor_pay_order_id=razorpay_payment['id'],order=order)
        #     payment.save()
        #     print(payment.id)

                # payment=Payment(user=user,)
    # cart=Cart.objects.get(user=request.user)
    # cart_items=CartItems.objects.filter(cart=cart)
    
    # address=get_object_or_404(UserProfile,id=address_id)
    cart=Cart.objects.get(user=user)
    coupon=cart.coupon
    if coupon:
        usercoupon=UserCoupons.objects.create(user=user,coupon=coupon,is_used=True)
    # cart.delete()
    context={
        'order':order,
        'payment':payment
    }
    return render(request,'user/payment-confirmation.html',context)


# def create_order(request,total=0,quantity=0):
#     user=request.user
#     address_id=None
#     order=None
#     payment=None
#     order_number=None
#     razorpay_payment=None
#     cart_items=CartItems.objects.filter(cart__user=user)
#     grand_total=0
#     tax=0
#     for cart_item in cart_items:
#         quantity=cart_item.quantity
#         total+=(cart_item.product.price * cart_item.quantity)
#     tax=(5*total)/100
#     grand_total = total+tax
#     if request.method == 'POST':
#         if 'checkout_submit' in request.POST:
#             print('after post')
#             address_id=request.POST.get('address')
#             try:
#                 address=UserProfile.objects.get(id=address_id)
#             except UserProfile.DoesNotExist:
#                 if not address_id:
#                     messages.info(request,'Please select an address ')
#                     return redirect('checkout')
#             create_order=Order.objects.create(user=user,address=address,order_total=grand_total)
#             create_order.save()
#             #generate order number

#             yr=int(datetime.date.today().strftime('%Y'))
#             dt=int(datetime.date.today().strftime('%d'))
#             mt=int(datetime.date.today().strftime('%m'))
#             d=datetime.date(yr,mt,dt)
#             current_date=d.strftime("%Y%m%d")
#             order_number=current_date+str(create_order.id)
#             create_order.order_number=order_number
#             create_order.save()
#             order = Order.objects.filter(user=user).order_by('-created_at').first()
#             order_sub_total=0
#             order_tax=0
#             order_toatl=0
#             discount=0
#             for cart_item in CartItems.objects.all():
#                 variants=cart_item.product
#                 order_sub_total=variants.price*cart_item.quantity
#                 order_tax=(5*order_sub_total)/100
#                 if cart_item.cart.coupon is None:
#                     discount_value=0
#                     order_toatl=order_sub_total+order_tax-discount_value
#                 else:
#                     discount_value=cart_item.cart.coupon.discount
#                     order_toatl=order_sub_total+order_tax-discount_value
#                 image=ProductImage.objects.filter(product_size=variants).first()
#                 order_items=OrderProduct.objects.create(order=order,user=user,product=cart_item.product,quantity=cart_item.quantity,product_image=image,product_price=variants.price,sub_total=order_sub_total,tax=order_tax,discount_price=discount_value,total_price=order_toatl)
#         if 'payment_submit' in request.POST:
#             print('elif111111111111111111111111111')
#             order = Order.objects.filter(user=user).order_by('-created_at').first()
#             payment_method=request.POST.get('pay-method')
#             if payment_method=='cod':
#                 payment=Payment.objects.create(user=user,payment_method=payment_method,order=order)
#                 payment.save()
#                 # pay=Payment.objects.get(order=order)
#                 # order_items=OrderProduct.objects.filter(order=order)
#                 # for item in order_items:
#                 #     item.payment=pay.id
#                 print('redirect445')
#                 return redirect('confirmation-cod' ,order.id)
#                 # elif payment_method=='razorpay':
#                 #     amount=grand_total
#                 #     load_dotenv()
#                 #     client=razorpay.Client(auth=(os.getenv('RAZOR_PAY_KEY_ID'),os.getenv('KEY_SECRET')))
#                 #     razorpay_payment=client.order.create({'amount':grand_total*100 , 'currency':'INR', 'payment_capture':1})
#                 #     payment=Payment.objects.create(user=user,payment_method=payment_method,amount_paid=grand_total,razor_pay_order_id=razorpay_payment.id,order=order)
#                 #     payment.save()
#             print('11111111111111111111111111111111111111111111111111111111')
#             try:
#                 print('2222222222222222222222222')
#                 payment=Payment.objects.get(order=order)
#             except Payment.DoesNotExist:
#                 print('2222222222222222222edacfffeadf222222')
#                 load_dotenv()
#                 client=razorpay.Client(auth=(os.getenv('RAZOR_PAY_KEY_ID'),os.getenv('KEY_SECRET')))
#                 razorpay_payment=client.order.create({'amount':grand_total*100 , 'currency':'INR', 'payment_capture':1})
#                 print(razorpay_payment)
#                 payment=Payment.objects.create(user=user,payment_method='razorpay',amount_paid=grand_total,razor_pay_order_id=razorpay_payment['id'],order=order)
#                 print(payment.id)
#                 payment.save()
#             #     try:
#             #     payment=Payment.objects.get(order=order)
#             #     print('2222222222222222222222222')
#             # except Payment.DoesNotExist:
#             #     print('2222222222222222222edacfffeadf222222')
#             #     load_dotenv()
#             #     client=razorpay.Client(auth=(os.getenv('RAZOR_PAY_KEY_ID'),os.getenv('KEY_SECRET')))
#             #     razorpay_payment=client.order.create({'amount':grand_total*100 , 'currency':'INR', 'payment_capture':1})
#             #     print(razorpay_payment)
#             #     payment=Payment.objects.create(user=user,payment_method='razorpay',amount_paid=grand_total,razor_pay_order_id=razorpay_payment['id'],order=order)
#             #     print(payment.id)
#             #     payment.save()
# # payment=Payment(user=user,)
#     # cart=Cart.objects.get(user=request.user)
#     # cart_items=CartItems.objects.filter(cart=cart)
    
#     # address=get_object_or_404(UserProfile,id=address_id)
#     amount=grand_total*100
#     context={
#         'order':order,
#         'payment':payment,
#         'amount':amount,
#         'razorpay_payment':razorpay_payment
#     }
#     return render(request,'user/payment-confirmation.html',context)


def confirmation_cod(request,id):
    order=Order.objects.get(pk=id)
    context={
        'order':order
    }
    return render(request,'user/confirmation-cod.html',context)


def my_order(request):
    user=request.user
    order=Order.objects.filter(user=user).order_by('-created_at')
    order_items=OrderProduct.objects.filter(order__in=order).order_by('-created_at')
    quantity=0
    for i in order_items:
        quantity+=i.quantity
    image=OrderProduct.objects.filter(order__in=order).order_by('-created_at').first()
    context={
        'user':user,
        'order':order,
        'order_items':order_items,
        'quantity':quantity,
        'image':image,
    }
    return render(request,'user/my-order.html',context)

def order_details(request,id):
    order_items=OrderProduct.objects.filter(order=id)
    order=Order.objects.get(pk=id)
    payment=Payment.objects.get(order=id)
    context={
        'order_items':order_items,
        'order':order, 
        'payment':payment, 
    }
    return render(request,'user/order-details.html',context)