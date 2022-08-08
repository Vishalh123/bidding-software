from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=200)
    date_joined = models.DateTimeField(
        verbose_name='datejoined', auto_now_add=True, null=True, blank=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    ifLogged = models.BooleanField(default=False)
    token = models.CharField(max_length=500, null=True, default="")
    profile = models.ImageField(null=True, blank=True, upload_to='profile', default=None)
    mobile_number = models.BigIntegerField(null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email


class AddProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='product_user')
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    max_bid = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class BidProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    product = models.ForeignKey(AddProduct, on_delete=models.CASCADE, related_name='user_product')
    bid_amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.bid_amount)

