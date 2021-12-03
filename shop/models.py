from django.db import models
from django.db.models.aggregates import Max
from django.db.models.base import Model
from django.conf import settings
from django.db.models.fields import BooleanField
from django.shortcuts import reverse
from django_countries.fields import CountryField
import os
from pathlib import Path

#things consider to change
# +discounted price
# store how the format to be of label (e.g. primary, ...)
# #use <del> for orig price

class Season_choice(models.Model):
    name=models.CharField(max_length=30, blank=True, null=True, unique=True)
    def __str__(self):
        return self.name

class Gender_choice(models.Model):
    name=models.CharField(max_length=30, blank=True, null=True, unique=True)
    def __str__(self):
        return self.name

class Type_choice(models.Model):
    gender_name=['Woman', 'Man', 'Both','Kid', 'All']
    gender_value=['Woman', 'Man', 'Both', 'Kids', 'All']
    gender_choice=list(zip(gender_name, gender_value))
    name=models.CharField(max_length=30, blank=True, null=True, unique=True)
    product_gender=models.ForeignKey(Gender_choice, on_delete=models.SET_NULL, null=True, blank=True)
    show_in_all_category=models.BooleanField(default=False)
    # product_gender=models.CharField(max_length=20, choices=Gender_choice, default='woman')
    def __str__(self):
        return f'{self.name} - {self.product_gender.name}'

#products to be sold in the website
class Item(models.Model):
    #choices
    season_name=['spring', 'summer', 'autum', 'winter', ]
    season_value=['spring', 'summer', 'autum', 'winter', ]
    season_choice=list(zip(season_name, season_value))
        
    type_name=['tee', 'shirt', 'jean', 'dress', 'trousers', 'jacket', ]
    type_value=['t-shirt', 'shirt', 'jeans', 'dresses', 'trousers', 'coats and jackets', ]
    type_choice=list(zip(type_name, type_value))

    gender_name=['female', 'male', 'neutral','kid']
    gender_value=['female', 'male', 'neutral', 'kids']
    gender_choice=list(zip(gender_name, gender_value))

    #label is like hit, new-arrival, best seller...
    label_name=['new','best','recom','sales',]
    label_value=['new-arrival','best-seller','recommended','sales',]
    label_choice=list(zip(label_name,label_value))
    #primary, secondary, danger???

    #necessary
    name = models.CharField(max_length=120)
    product_season=models.ForeignKey(Season_choice, on_delete=models.CASCADE)
    product_type=models.ForeignKey(Type_choice, on_delete=models.CASCADE)
    product_gender=models.ForeignKey(Gender_choice, on_delete=models.CASCADE)
    # product_season=models.CharField(choices=season_choice, max_length=10)
    # product_type=models.CharField(choices=type_choice, max_length=20)
    # product_gender=models.CharField(choices=gender_choice, max_length=20, default='female')
    price = models.DecimalField(max_digits=20, decimal_places=2)
            #os.path.join, cannot have '/', only '<words>', it will add the '/' for you
    image = models.ImageField(upload_to='product_images', height_field='image_height', width_field='image_width', 
        default=os.path.join(settings.MEDIA_DIR,"product_images", "white_tshirt.jpg")) 
    # image = models.ImageField(upload_to='product_images', height_field='image_height', width_field='image_width', ) 
    #necessary but with default
    stock=models.IntegerField(default=0)
    #Not necessary
    discounted_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    label = models.CharField(choices=label_choice, max_length=20, blank=True,  null=True)
    description = models.TextField(blank=True, null=True)
    #place holder?
    image_height=models.PositiveIntegerField(default=1200)
    image_width=models.PositiveIntegerField(default=900)

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
        return f'{self.user.username}: {self.quantity} of {self.item.name} - {self.paid}'

    def name_for_order(self):
        return f'{self.item.name} * {self.quantity}'

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
    orderitems=models.ManyToManyField(OrderItem, related_name='orderitems')
    #date of purchase
    orderDate = models.DateTimeField(blank=True, null=True)
    #is the order fulfilled
    complete = models.BooleanField(default=False)
    ship_addr=models.ForeignKey('Address', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}: order {self.pk}'

    def get_total_price(self):
        total_price=0
        for an_item in self.orderitems.all(): 
            total_price+=an_item.get_order_item_price()
        return total_price

class Address(models.Model):
    #2 kinds of addr
    ADDRESS_CHOICE = [('b', 'billing'), ('s', 'shipping')]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, )
    address_type=models.CharField(max_length=10, choices=ADDRESS_CHOICE, default='s')
    address_line1=models.CharField(max_length=100)
    address_line2=models.CharField(max_length=100, blank=True, null=True)
    address_line3=models.CharField(max_length=100, blank=True, null=True)
    country=CountryField()
    zip_code=models.CharField(max_length=20)
    def __str__(self): 
        return f'zip:{self.zip_code}, country:{self.country},{self.address_line1},{self.address_line2},{self.address_line3}'

#for shop owner access to store, is meant to NOT open to register (only admin can set)
class UserProfile(models.Model):
    #using choice field NOT bool field -> allow adding more roles
    #only after django 3
    #class role_choice(models.TextChoices):
    #    STAFF='staff'
    #    CUSTOMER='customer'
    role_choice=[('customer','customer'), ('staff','staff'), ]
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    roles = models.CharField(max_length=20, choices=role_choice, default=role_choice[0][0])

    def __str__(self):
        return self.user.username

#class storeConfig(models.Model):

class homepage_config(models.Model):
    type_choice=Item.type_choice

    #the banner and its slogan
    banner_image=models.ImageField(upload_to='homepage_images', default=os.path.join(settings.MEDIA_DIR,"homepage_images", "autum1.jpg"))
    # banner_image=models.ImageField(upload_to='homepage_images', blank=True, null=True)   
    slogan_line1=models.CharField(max_length=100, default='READY FOR')
    slogan_line2=models.CharField(max_length=100, blank=True, null=True, default='WINTER?')
    slogan_line3=models.CharField(max_length=100, blank=True, null=True)
    #the 3 featured categories
    category_image1=models.ImageField(upload_to='feature_product', default=os.path.join(settings.MEDIA_DIR,"feature_product", "shirt1_square.jpg"))
    # category_image1=models.ImageField(upload_to='feature_product', blank=True, null=True)
    # category1=models.CharField(max_length=100, choices=type_choice, default='shirt')
    category1=models.ForeignKey(Type_choice, on_delete=models.SET_NULL, null=True, blank=True, related_name='cate1_type')
    
    category_image2=models.ImageField(upload_to='feature_product', default=os.path.join(settings.MEDIA_DIR,"feature_product", "jean1_square.jpg"))
    # category_image2=models.ImageField(upload_to='feature_product', blank=True, null=True)
    # category2=models.CharField(max_length=100, choices=type_choice,default='trousers')
    category2=models.ForeignKey(Type_choice, on_delete=models.SET_NULL, null=True, blank=True, related_name='cate2_type')

    category_image3=models.ImageField(upload_to='feature_product', default=os.path.join(settings.MEDIA_DIR,"feature_product", "dress1_square.jpg"))
    # category_image3=models.ImageField(upload_to='feature_product', blank=True, null=True)
    # category3=models.CharField(max_length=100, choices=type_choice, default='dress')
    category3=models.ForeignKey(Type_choice, on_delete=models.SET_NULL, null=True, blank=True, related_name='cate3_type')

class contact_us_config(models.Model):
    profile_image = models.ImageField(upload_to='contact_us', default=os.path.join(settings.MEDIA_DIR,"contact_us", "shirt1_square.jpg"))
    # profile_image = models.ImageField(upload_to='contact_us', blank=True, null=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    portal1_image=models.ImageField(upload_to='contact_us', blank=True, null=True)
    portal1_link=models.URLField(max_length=200, blank=True, null=True)
    portal2_image=models.ImageField(upload_to='contact_us', blank=True, null=True)
    portal2_link=models.URLField(max_length=200, blank=True, null=True)
    portal3_image=models.ImageField(upload_to='contact_us', blank=True, null=True)
    portal3_link=models.URLField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.title

class shop_config (models.Model):
    instagram = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    google_play = models.URLField(max_length=200, blank=True, null=True)
    paypal_account = models.CharField(max_length=200, blank=True, null=True)
    shop_icon = models.ImageField(upload_to='contact_us', blank=True, null=True)
    def __str__(self):
        return self.paypal_account


#it is the link with cover photo in contact us page
class page_link(models.Model):
    title = models.CharField(max_length=50)
    cover_image = models.ImageField(upload_to='contact_us')
    link = models.URLField(max_length=200)
    description = models.TextField()
    contact_us = models.ForeignKey(contact_us_config, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class navbar_dropdown_category(models.Model):
    type_choice=Item.type_choice
    category_name=models.CharField(max_length=100, choices=type_choice, unique=True)

class navbar_dropdown_config(models.Model):
    name=models.CharField(max_length=20)
    categories=models.ManyToManyField(navbar_dropdown_category)



    
