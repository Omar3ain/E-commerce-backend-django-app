from django.db import models
from order.models import Order
# Create your models here.
class Payment(models.Model):
    amount = models.FloatField()
    currency = models.CharField(max_length=3)
    stripe_charge_id = models.CharField(max_length=50, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255,default='PENDING')
    def __str__(self):
        return self.stripe_charge_id