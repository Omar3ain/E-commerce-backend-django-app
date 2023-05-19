from django.db import models
from category.models import Category

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    main_image = models.ImageField(upload_to='products', null=True, blank=True)
    image_urls = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.main_image:
            image_url = self.main_image.url
            if self.image_urls:
                self.image_urls += f',{image_url}'
            else:
                self.image_urls = image_url

        super().save(*args, **kwargs)