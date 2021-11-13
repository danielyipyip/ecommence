import re
from django import forms
from django.forms.widgets import Textarea
from .models import Item, OrderItem, Order, homepage_config, Address, navbar_dropdown_category, navbar_dropdown_config
from django_countries.fields import CountryField

class CheckoutForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=['address_line1', 'address_line2', 'address_line3', 'country', 'zip_code', ]
#didn't include: 'address_type'


class addProductForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=['name', 'product_season', 'product_type', 'price', 'discounted_price', 'label', 'description', 'image', 'stock']

class homepage_config_form(forms.ModelForm):
    class Meta:
        model=homepage_config
        fields=['banner_image','slogan_line1','slogan_line2','slogan_line3', 'category_image1', 'category1', 
            'category_image2', 'category2', 'category_image3', 'category3']

class navbar_dropdown_form(forms.ModelForm):
    class Meta:
        model=navbar_dropdown_config
        fields=['name', 'categories']

        