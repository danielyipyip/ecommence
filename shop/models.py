from django.db import models
from django.db.models.aggregates import Max
from django.db.models.base import Model
from django.conf import settings
from django.shortcuts import reverse
from django_countries.fields import CountryField

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
        ('trousers', 'trousers'), 
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
    discounted_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    label = models.CharField(choices=label_choice, max_length=20, blank=True,  null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='product_images', blank=True, height_field='image_height', width_field='image_width')
    stock=models.IntegerField(default=0)
    image_height=models.PositiveIntegerField(default=600)
    image_width=models.PositiveIntegerField(default=600)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product-detail', kwargs={'pk': self.id})

    def get_add_to_cart_url(self):
        return reverse('shop:add_to_cart_product_detail', kwargs={'pk': self.id})

    def get_remove_from_cart_url(self):
        return reverse('shop:remove_from_cart', kwargs={'pk': self.id})

#item in an order (split because of M:M relationship)
class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    #can re-order, paid and in cart is different
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}: {self.quantity} of {self.item.name}'

    def get_order_item_price(self):
        if self.item.discounted_price:
            return self.quantity*self.item.discounted_price
        return self.quantity*self.item.price

    def get_discount_amount(self):
        return self.quantity*self.item.price-self.quantity*self.item.discounted_price

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

    ship_addr=models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total_price=0
        for an_item in self.orderitems.all(): 
            total_price+=an_item.get_order_item_price()
        return total_price

class Address(models.Model):
    #2 kinds of addr
    ADDRESS_CHOICE = [('b', 'billing'), ('s', 'shipping')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address_type=models.CharField(max_length=10, choices=ADDRESS_CHOICE)
    addr1=models.CharField(max_length=100)
    addr2=models.CharField(max_length=100, blank=True, null=True)
    addr3=models.CharField(max_length=100, blank=True, null=True)
    country=CountryField()
    zip_code=models.CharField(max_length=20)

