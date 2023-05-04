from django.db import models
from category.models import Category

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    main_image = models.TextField(blank=True)
    image_urls = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name