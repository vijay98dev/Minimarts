from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from account.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.models import CustomUser
from category.models import Category
from store.models import Product,ProductImage,ProductSize
from django.utils.text import slugify




# Create your views here.
def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('admin-dashboard')
        if request.method=='POST':
            email=request.POST["email"]
            password=request.POST['password']
            user=CustomUser.objects.filter(email=email)
            if not user.exists():
                messages.success(request,'Account not found')
                return redirect('admin-login')
            user=authenticate(email=email,password=password)
            if user and user.is_superuser:
                login(request,user)
                return redirect('admin-dashboard')
            
            messages.error(request,'Invalid Password')
            return redirect('admin-login')

        return render(request,'admin/admin-login.html')
    except Exception as e:
        print(e)
    return render(request,'admin/admin-login.html')


def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html')

@login_required(login_url='login')
def admin_logout(request):
    logout(request)
    messages.success(request,'Logout successful')
    return redirect('admin-login')

def userlist(request):
    user=CustomUser.objects.all()
    context={
        'users':user
    }
    return render (request,'admin/userlist.html',context)


def blockuser(request,id):
    user=get_object_or_404(CustomUser,pk=id)
    
    # user_id=request.GET.get('id')
    # user=CustomUser.objects.get(pk=user_id)
    user.is_active=False
    user.save()
    return redirect('users')

def unblockuser(request,id):
    user=get_object_or_404(CustomUser,pk=id)
    # user_id=request.GET.get('id')
    # user=CustomUser.objects.get(pk=user_id)
    user.is_active=True
    user.save()
    return redirect('users')

def categories(request):
    category=Category.objects.all()
    context={
        'categories':category
    }
    return render(request,'admin/category.html',context)

def delete_category(request,id):
    category=get_object_or_404(Category,pk=id)
    category.delete()
    return redirect('categories')

def add_category(request):
    if request.method=='POST':
        category_name=request.POST['category_name']
        description=request.POST['description']
        slug=slugify(category_name)
        if Category.objects.filter(category_name=category_name).exists():
            error_message = 'Category name already exists.'
            return render(request, 'admin/add-category.html', {'error_message': error_message})
        else:
            category = Category(category_name=category_name,description=description,slug=slug)
            category.save()
        return redirect('categories')
    return render(request, "admin/add-category.html")


def edit_category(request,id):
    categories=Category.objects.get(pk=id)
    if request.method=='POST':
        category_name=request.POST.get('category')
        description=request.POST.get('description')
        slug=slugify(category_name)
        if Category.objects.filter(category_name=category_name).exclude(pk=id).exists():
            messages.error(request,'Category name already exists')
            return redirect('categories')
        else:
            categories.category_name = category_name
            categories.description = description
            categories.slug = slug
            categories.save()
        return redirect('categories')
    context={'category':categories}
    return render(request,'admin/edit-category.html',context)

def product(request):
    product=ProductImage.objects.all()
    context={
        'products':product
    }
    return render(request,'admin/product.html',context)


def add_product(request):
    if request.method=='POST':
        product_name=request.POST.get('product_name')
        description=request.POST.get('description')
        size=request.POST.get('size')
        price=request.POST.get('price')
        uploaded_image=request.FILES.getlist('image') 
        stock=request.POST.get('stock')  
        category_id=request.POST.get('category')  
        if Product.objects.filter(product_name=product_name).exists():
            messages.error(request,'Product name is already exists')
            return redirect('add-product')
        else:
            selected_category=get_object_or_404(Category,id=category_id)
            if size:
                size=float(size)
            product = Product.objects.create(product_name=product_name,description=description,category=selected_category)
            # product.save()
            size_product=ProductSize.objects.create(price=price,stock=stock,product_size=size,product=product)
            # size_product.save()
            # print(size_product)
            for images in uploaded_image:
                images=ProductImage.objects.create(product_image=images,product=product,product_size=size_product)
                # images.save()
            messages.success(request,'Product added successfully')
            return redirect('product')
    categories=Category.objects.all()
    context={
        'categories':categories
    }
    return render(request,'admin/add-product.html',context)


def delete_product(request,id):
    product=get_object_or_404(ProductSize,id=id)
    product.soft_delete()
    return redirect('product')

def edit_product(request,id):
    product=ProductSize.objects.get(pk=id)
    # if request.method=='POST':
    #     name=request.POST.get('product_name')
    #     description=request.POST.get('description')
    #     category=request.POST.get('category')
    #     if Product.objects.filter(product_name=name).exists:
    #         messages.error(request,'Product name already exists')
    #         return redirect('product')
    #     # else:
    #     #     product.product_name=
    context={
        'products':product
    }
    return render(request,'admin/edit-product.html',context)