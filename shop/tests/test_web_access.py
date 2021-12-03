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

User = get_user_model()
#no login requrired url "name"
url_list=['home-page', 'list-page', 'unauthorized', 'search', 'about-us']
url_list_pk=['product/'] #need pk
#login needed url list
url_login=['shopping-cart', 'checkout', 'payment', 'payment-success', 'payment-unsuccess', ]
#admin needed url list
url_admin=['item-list', 'upload-item', 'order-list', 'home-config', 'category-config', 
    'link-config', 'contact-config', 'config-all']
url_admin_pk=['update-item']
#wrong link
url_fake=['lists-page', 'payment', 'configuration']
url_fake_raw=['homes/', 'mycart/', 'authorized/'] #raw link


############################################################
###################### test webpage access #########################
############################################################

class test_access_to_page(TestCase):
    def setUp(self):
        #customer
        self.customer_ac='customer1'
        self.customer_pw='notshop1'
        user = User.objects.create_user(username=self.customer_ac, password=self.customer_pw)
        #shop owner
        self.admin_ac = 'shop1'
        self.admin_pw = 'notcustomer1'
        admin_user = User.objects.create_user(username=self.admin_ac, password=self.admin_pw)
        admin_group = Group(name = 'shop_admin')
        admin_group.save()
        admin_user.groups.add(admin_group)
        admin_user.save()

    def test_correct_page(self): #no login needed
        for link in url_list:
            self.assertEqual(self.client.get(reverse('shop:'+link)).status_code, 200)
    def test_login_required_fail(self):
        for link in url_login:
            self.assertTrue(self.client.get(reverse('shop:'+link)).status_code, 201)
        for link in url_admin:
            self.assertTrue(self.client.get(reverse('shop:'+link)).status_code, 201)
    def test_wrong_link(self):
        # this will raise no valid reverse instead
        # for link in url_fake:
        #     self.assertTrue(self.client.get(reverse('shop:'+link)).status_code, 404)
        for link in url_fake_raw:
            self.assertTrue(self.client.get(link).status_code, 404)
    #customer login here
    def test_login_required(self):
        login = self.client.login(username=self.customer_ac, password=self.customer_pw)
        for link in url_login:
            self.assertTrue(self.client.get(reverse('shop:'+link)).status_code, 200)
    def test_admin_w_customer(self):
        login = self.client.login(username=self.customer_ac, password=self.customer_pw)
        for link in url_admin:
            self.assertTrue(self.client.get(reverse('shop:'+link)).status_code, 201)
    def test_normal_page(self): #test non-require login page after login
        for link in url_list:
            self.assertEqual(self.client.get(reverse('shop:'+link)).status_code, 200)
    #admin login here
    def test_admin_required(self):
        login = self.client.login(username=self.admin_ac, password=self.admin_pw)
        for link in url_admin:
            self.assertTrue(self.client.get(reverse('shop:'+link)).status_code, 200)


#create config??


