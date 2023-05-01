from django.db import models
from products.models import Product
from users.models import User
STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SHIPPING', 'Shipping'),
        ('DELIVERED', 'Delivered'),
]

class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_CHOICES[0])
    createdAt = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
