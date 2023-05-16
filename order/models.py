from django.db import models
from products.models import Product
from users.models import User
from django_countries.fields import CountryField

STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SHIPPING', 'Shipping'),
        ('DELIVERED', 'Delivered'),
]

class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    country = CountryField(null=True)
    city = models.TextField(null=True)
    street_name = models.TextField(null=True)
    building_no =models.IntegerField(null=True)
    floor_no =models.IntegerField(null=True)    
    apartment_no =models.IntegerField(null=True)   
    createdAt = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
