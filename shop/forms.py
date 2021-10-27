import re
from django import forms
from django.forms.widgets import Textarea
from .models import Item, OrderItem, Order
from django_countries.fields import CountryField

class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = (
    ('C', 'Credit/debit card'),
    ('P', 'PayPal')
    )
    ship_addr1=forms.CharField()
    ship_addr2=forms.CharField(required=False)
    ship_addr3=forms.CharField(required=False)
    ship_country=CountryField().formfield()
    ship_zip=forms.CharField()

    #bill_addr1=forms.CharField()
    #bill_addr2=forms.CharField(required=False)
    #bill_addr3=forms.CharField(required=False)
    #bill_country=CountryField()

    #same_billing_address = forms.BooleanField(required=False)
    #set_default_shipping = forms.BooleanField(required=False)
    #use_default_shipping = forms.BooleanField(required=False)
    #set_default_billing = forms.BooleanField(required=False)
    #use_default_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class addProductForm(forms.ModelForm):
    class Meta:
        model=Item
        fields=['name', 'product_season', 'product_type', 'price', 'discounted_price', 'label', 'description', 'image', 'stock']