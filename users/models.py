from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        username = self.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

    def normalize_username(self, username):
        """
        Normalize the username by lowercasing it.
        """
        return username.lower()

class User(AbstractBaseUser):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='./user_images', null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_module_perms(self, app_label):
        # return True if the user has any permissions for the given app label
        return self.is_active and self.is_staff

    def has_perm(self, perm, obj=None):
        # return True if the user has the specified permission
        return self.is_active and self.is_superuser
    
# class Token(models.Model):
#     key = models.CharField(max_length=40, primary_key=True)
#     user = models.OneToOneField(User, related_name='user_tokens', on_delete=models.CASCADE)
#     created = models.DateTimeField(auto_now_add=True)