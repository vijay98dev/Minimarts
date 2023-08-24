from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,ProductImage,ProductSize
from django.db.models import Q
from category.models import Category
from django.http import Http404
from cart.models import Cart,CartItems
from cart.views import _cart_id
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
        # print(single_product)
        data=ProductSize.objects.all().filter(slug=product_slug)
        print(data)
        in_cart=CartItems.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        single_product=ProductImage.objects.filter( product__category__slug=category_slug,product_size__slug=product_slug)
        # data=ProductImage.objects.filter(product_size=single_product)
        # in_cart=CartItems.objects.filter(cart__cart_id=_cart_id(request),product__product_size=single_product).exists()
    except ProductImage.DoesNotExist:
        raise Http404("Product not found")
    context={
        'single_product':single_product,
        'data':data,
        'in_cart':in_cart,
        # 'data':data,
        # 'in_cart':in_cart,
    }
    return render(request,'user/product_details.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        print(keyword,'2368726348621938691273412937498')
        if keyword:
            print(keyword,'2368726348621938691273412937498')
            product=ProductImage.objects.filter(Q(product__product_name__icontains=keyword) | Q(product__description__icontains=keyword) | Q(product__category__category_name__icontains=keyword) | Q(product_size__price__icontains=keyword))
        context={
            'products':product
        }
    return render(request,'user/search.html',context)

