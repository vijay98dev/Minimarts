from django.db import models
from category.models import Category
from django.utils.text import slugify

# Create your models here.
class Product(models.Model):
    product_name=models.CharField(max_length=50,unique=True)        
    description=models.TextField(max_length=400,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.product_name
    

class ProductSize(models.Model):
    product_size=models.FloatField(max_length=5,unique=True,blank=False)
    price=models.IntegerField()
    stock=models.IntegerField()
    is_available=models.BooleanField(default=True)
    is_delete=models.BooleanField(default=False)
    modified_date=models.DateTimeField(auto_now=True)
    slug=models.SlugField(max_length=100,unique=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.product_size


    def soft_delete(self):
        self.is_delete=True
        self.save()


    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.product.product_name} {self.product_size}")
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product_image=models.ImageField(upload_to='photos/products', height_field=None, width_field=None, max_length=None)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size=models.ForeignKey(ProductSize, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.product_image