from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    


class Wishlist(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    user_id = models.ForeignKey('users.User', on_delete=models.CASCADE)
