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

#from other tests
from .test_model import setup_items

############################################################
###################### test webpage content #########################
############################################################
####### user side #######

#go to home
class test_homepage(TestCase):
    def setUp(self):
        shirt, tee = setup_items(self) #tee have recomm
        self.recom_item=tee
    def test_load_item(self):
        request = RequestFactory().get(reverse('shop:home-page'))
        response = home(request)
        # view.setup(request)
        # self.assertIn(self.recom_item, response.content)


#go to browse

#search an item

#go to product detail

#add >1 item to cart

#increase amount

#reduce amount

#remoce item

#checkout

#pay


####### owner side #######
#add item

#modify item

#delete item

#manage order

#change layout

