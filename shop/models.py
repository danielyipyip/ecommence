from django.db import models
from django.db.models.aggregates import Max
from django.db.models.base import Model
from django.conf import settings
from django.shortcuts import reverse

#things consider to change
# +discounted price
# store how the format to be of label (e.g. primary, ...)
# #use <del> for orig price

#products to be sold in the website
class Item(models.Model):
    #choices
    season_choice=[
        ('spring', 'spring'), 
        ('summer', 'summer'), 
        ('autum', 'autum'), 
        ('winter', 'winter'), 
    ]
        
    type_choice=[
        ('tee', 't-shirt'), 
        ('shirt', 'shirt'), 
        ('jean', 'jeans'), 
        ('dress', 'dresses'), 
        ('jacket', 'coats and jackets'), 
    ]

    #label is like hit, new-arrival, best seller...
    label_choice=[
        ('new', 'new-arrival'), 
        ('best', 'best-seller'), 
        ('recom', 'recommended'), 
        ('sales', 'sales'), 
    ]
    #primary, secondary, danger???

    #basic config of an item
    name = models.CharField(max_length=120)
    product_season=models.CharField(choices=season_choice, max_length=10)
    product_type=models.CharField(choices=type_choice, max_length=20)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    label = models.CharField(choices=label_choice, max_length=20, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product-detail', kwargs={'pk': self.id})

    def get_add_to_cart_url(self):
        return reverse('shop:add_to_cart', kwargs={'pk': self.id})

#item in an order (split because of M:M relationship)
class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    #can re-order, paid and in cart is different
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} of {self.item.name}'

#a purchase order
class Order(models.Model):
    #model is associated with a user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #is the order paid; when created, is not
    paid = models.BooleanField(default=False)
    #content of an order
    orderitems=models.ManyToManyField(OrderItem)
    #date of purchase
    orderDate = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username


