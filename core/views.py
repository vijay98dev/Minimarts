from django.shortcuts import render
from store.models import Product,ProductImage,ProductSize
from orders.models import Order,Payment,OrderProduct



# Create your views here.
def index(request):
    product=ProductImage.objects.all()
    
    context={
        'products':product
    }
    return render(request,'user/index.html',context)


def invoice(request,id):
    user=request.user
    order=Order.objects.get(pk=id)
    print(order)
    order_items=OrderProduct.objects.filter(order=order)
    print(order_items)
    payment=Payment.objects.get(order=order)
    print(payment.id)
    context={
        'order':order,
        'order_items':order_items, 
        'payment':payment, 
    }
    return render(request,'user/invoice.html',context)