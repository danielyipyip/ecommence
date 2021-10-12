from django.db import models
from django.db.models.aggregates import Max
from django.db.models.base import Model
from django.conf import settings

# Create your models here.

#products to be sold in the website
class Item(models.Model):
    #basic config of an item
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images', blank=True)

    def __str__(self):
        return self.name

#item in an order (split because of M:M relationship)
class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

#a purchase order
class Order(models.Model):
    #model is associated with a user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #is the order placed; when created, is not
    placed = models.BooleanField(default=False)
    #content of an order
    items=models.ManyToManyField(OrderItem)
    orderDate = models.DateTimeField()

    def __str__(self):
        return self.user.username


