from django.db import models
from account.models import CustomUser
from store.models import Product,ProductImage,ProductSize


# Create your models here.

class Cart(models.Model):
    cart_id=models.CharField(max_length=250,blank=True)
    user=models.ForeignKey("account.Customuser", on_delete=models.CASCADE)
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart for {self.user.username}'
    



class CartItems(models.Model):
    cart=models.ForeignKey("cart.Cart",on_delete=models.CASCADE)
    product=models.ForeignKey("store.ProductSize",on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)


    def __str__(self) -> str:
        return f'{self.product.product.product_name} -{self.quantity}'
    

    def sub_total(self):
        return self.product.price * self.quantity
    
    
class Wishlist(models.Model):
    user=models.ForeignKey("account.CustomUser",  on_delete=models.CASCADE)
    product=models.ForeignKey("store.ProductSize", on_delete=models.CASCADE)