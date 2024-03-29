from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class userauthenticate(AbstractUser):
    username = None
    email = models.CharField(max_length=122, unique=True)
    name = models.CharField(max_length=255)  # New field for storing user's name
    password = models.CharField(max_length=122)
    is_subscribe = models.BooleanField(default=False)
    counter = models.IntegerField(default=2, null=True, blank=True)
    subscription_id = models.CharField(max_length=254, null=True, blank=True)
    subscription_id2 = models.CharField(max_length=254, null=True, blank=True)  # New field for storing subscription ID
    customer_id = models.CharField(max_length=254, null=True, blank=True)
    First = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []



class Visitor(models.Model):
    ip_address   = models.CharField(max_length=100)
    country_name = models.CharField(max_length=100)
    coordinates  = models.CharField(max_length=100)
    city         = models.CharField(max_length=100)
    timestamp    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.country_name} - {self.timestamp}"
    
class Visitor1(models.Model):
    ip_address   = models.CharField(max_length=100)
    country_name = models.CharField(max_length=100)
    coordinates  = models.CharField(max_length=100)
    city         = models.CharField(max_length=100)
    timestamp    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} - {self.country_name} - {self.timestamp}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AdminCategory(models.Model):
    country_name = models.CharField(max_length=100)