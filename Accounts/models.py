from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)


from Ecommerce.models import *


class Address(models.Model):
    ADDRESS_TYPES = [
        ('billing', 'Billing'),
        ('shipping', 'Shipping')
    ]
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey('Ecommerce.Order', on_delete=models.SET_NULL, blank=True, null=True)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPES)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=120)
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, null=True, blank=True)
    postal_code = models.CharField(max_length=16)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=120)

    class Meta:
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return str(self.customer) + ' : ' + str(self.address_type).upper()

    def get_address(self):
        return f"{self.address_line_1} {self.address_line_2 or ''} / {self.state}, {self.postal_code} {self.city} {self.country}"
