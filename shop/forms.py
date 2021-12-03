import re
from django import forms
from django.forms.widgets import Textarea,  TextInput
from .models import Item, OrderItem, Order, homepage_config, Address, navbar_dropdown_category, navbar_dropdown_config, contact_us_config, page_link, Season_choice, Type_choice, Gender_choice,shop_config
from django_countries.fields import CountryField

#fields='__all__' then is all, no need write 1 by 1

class CheckoutForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=['address_line1', 'address_line2', 'address_line3', 'country', 'zip_code', ]
#didn't include: 'address_type'


class addProductForm(forms.ModelForm):
    class Meta:
        model=Item
        fields='__all__' 
        # fields=['name', 'product_season', 'product_type', 'price', 'discounted_price', 'label', 'description', 'image', 'stock']
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }
class homepage_config_form(forms.ModelForm):
    class Meta:
        model=homepage_config
        fields=['banner_image','slogan_line1','slogan_line2','slogan_line3', 'category_image1', 'category1', 
            'category_image2', 'category2', 'category_image3', 'category3']

class navbar_dropdown_form(forms.ModelForm):
    class Meta:
        model=navbar_dropdown_config
        fields=['name', 'categories']

class contact_us_config_form(forms.ModelForm):
    class Meta:
        model=contact_us_config
        fields=['profile_image','title','text', 'portal1_image', 'portal1_link', 
        'portal2_image', 'portal2_link', 'portal3_image', 'portal3_link', ]

class modify_order_form(forms.ModelForm):
    class Meta:
        model=Order
        fields=['user', 'paid', 'orderitems', 'orderDate', 'complete', 'ship_addr']

class page_link_form(forms.ModelForm):
    class Meta:
        model=page_link
        fields=['title','cover_image','link','description','contact_us']

class season_choice_form(forms.ModelForm):
    class Meta: 
        model=Season_choice
        fields=['name']

class type_choice_form(forms.ModelForm):
    class Meta: 
        model=Type_choice
        fields=['name', 'product_gender', 'show_in_all_category']

class gender_choice_form(forms.ModelForm):
    class Meta: 
        model=Gender_choice
        fields=['name']

class item_quantity(forms.Form):
    quantity= forms.IntegerField()

class shop_config_form(forms.ModelForm):
    class Meta:
        model=shop_config
        fields='__all__'
        # fields=['instagram', 'twitter', 'facebook', 'google_play', 'paypal_account','shop_icon']