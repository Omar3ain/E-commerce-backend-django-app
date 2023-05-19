from django.db import models

# Create your models here.
class Wishlist(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    user_id = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return f"Wishlist of user {self.user_id.username} for product {self.product.name}"
