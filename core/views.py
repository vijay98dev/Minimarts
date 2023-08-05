from django.shortcuts import render
from store.models import Product,ProductImage,ProductSize



# Create your views here.
def index(request):
    product=ProductImage.objects.all()
    
    context={
        'products':product
    }
    return render(request,'user/index.html',context)