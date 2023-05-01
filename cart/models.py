from django.db import models
from users.models import User
from products.models import Product

# Create your models here.
class Cart(models.Model):
   user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class CartItem(models.Model):
   product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
   cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
   quantity = models.IntegerField()