from django.db import models
from account.models import CustomUser,UserProfile
from django.utils.text import slugify
from store.models import ProductSize,ProductImage



# Create your models here.
class Payment(models.Model):
    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    )
 
    user=models.ForeignKey("account.CustomUser", on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=100)
    payment_method=models.CharField( max_length=100)
    amount_paid=models.CharField( max_length=100)
    status=models.CharField( max_length=100,choices=PAYMENT_STATUS,default='Pending')
    created_at=models.DateTimeField(  auto_now_add=True)


    def __str__(self):
        return self.payment_id
    

class Order(models.Model):
    ORDER_STATUS = (
    ('Processing','Processing'),
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Cancelled', 'Cancelled'),
    ('Out for Delivery', 'Out for Delivery'),
    ('Delivered', 'Delivered'),
   )
    

    user=models.ForeignKey("account.CustomUser",  on_delete=models.SET_NULL,null=True)
    payment=models.ForeignKey("orders.Payment",  on_delete=models.SET_NULL,null=True,blank=True)
    order_number=models.CharField( max_length=50)
    address=models.ForeignKey("account.UserProfile",  on_delete=models.DO_NOTHING)
    order_total=models.DecimalField( max_digits=10, decimal_places=2)
    status=models.CharField( max_length=50,choices=ORDER_STATUS,default='Processing')
    created_at=models.DateTimeField( auto_now_add=True)
    slug  = models.CharField(max_length=200,null=True,blank=True)


    def __str__(self):
        return f"Order {self.pk} for {self.user.user_name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.user.id) +str(self.created_at))
        return super().save(*args, **kwargs)


class OrderProduct(models.Model):
    order=models.ForeignKey("orders.Order",  on_delete=models.CASCADE)
    payment=models.ForeignKey("orders.Payment", on_delete=models.SET_NULL,blank=True,null=True)
    user=models.ForeignKey("account.CustomUser",  on_delete=models.CASCADE)
    product=models.ForeignKey("store.ProductSize",  on_delete=models.CASCADE)
    product_image=models.ForeignKey("store.ProductImage",  on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)
    product_price=models.DecimalField(max_digits=10, decimal_places=2)
    created_at=models.DateTimeField( auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True )


   
    def __str__(self):
        return f"{self.product.product.product_name} - {self.quantity}"