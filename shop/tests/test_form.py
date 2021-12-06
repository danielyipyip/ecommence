from django.test import TestCase, testcases, RequestFactory
from shop.models import (
    Item, Order, OrderItem, Address, homepage_config, navbar_dropdown_config, Season_choice, Type_choice, 
    Gender_choice, contact_us_config, page_link, shop_config)
from shop.forms import (CheckoutForm, addProductForm, homepage_config_form, item_quantity, contact_us_config_form, 
page_link_form, season_choice_form, type_choice_form, gender_choice_form, shop_config_form)
from shop.views import (home, )
#for allauth
from django.test.client import Client
from django.shortcuts import reverse
from allauth.utils import get_user_model
from django.contrib.auth.models import Group

class test_checkoutForms(TestCase):
    def test_valid_form(self):
        w = Address.objects.create(address_line1='Glasgow', address_line2='', address_line3='', 
        country='US', zip_code="G1")
        data = {'address_line1': w.address_line1, 'address_line2':w.address_line2, 
        'address_line3':w.address_line3, 'country': w.country, 'zip_code':w.zip_code}
        form = CheckoutForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        w = Address.objects.create(address_line1='', address_line2='', address_line3='', 
        country='UK', zip_code="G1")
        data = {'address_line1': w.address_line1, 'address_line2':w.address_line2, 
        'address_line3':w.address_line3, 'country': w.country, 'zip_code':w.zip_code}
        form = CheckoutForm(data=data)
        self.assertFalse(form.is_valid())