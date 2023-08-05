from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,ProductImage,ProductSize
from django.db.models import Q
from category.models import Category
# Create your views here.

def store(request,category_slug=None):
    categories=Category.objects.all()
    products=None
    product_counts=Product.objects.all().count()
    if category_slug is not None:
        category=get_object_or_404(Category,slug=category_slug)
        products=ProductImage.objects.all().filter(product__category__slug=category_slug,product_size__is_available=True)
    else:
        products=ProductImage.objects.filter(product_size__is_available=True)
    context={
        'product':products,
        'product_counts':product_counts,
        'categories':categories
    }
    return render(request,'user/store.html',context)

def product_details(request,category_slug,product_slug):
    try:
        single_product=ProductImage.objects.get(product__category__slug=category_slug,product_size__slug=product_slug)
    except Exception as e:
        raise e
    context={
        'single_product':single_product
    }
    return render(request,'user/product_details.html',context)