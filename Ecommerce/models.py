from django.db import models

# Create your models here.
from Accounts.models import Customer


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.name) + ' ' + str(self.price) + " €"

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    completed = models.BooleanField()

    def __str__(self):
        return str(self.id)

    @property
    def cart_total_price(self):
        orderproducts = self.orderproduct_set.all()
        total = sum([product.product_total_price for product in orderproducts])
        return total

    @property
    def cart_total_items(self):
        orderproducts = self.orderproduct_set.all()
        total = sum([product.quantity for product in orderproducts])
        return total


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    quantity = models.PositiveSmallIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'OrderProducts'

    def __str__(self):
        return str(self.product) + " x " + str(self.quantity)

    @property
    def product_total_price(self):
        return self.product.price * self.quantity

