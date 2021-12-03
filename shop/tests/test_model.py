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
############################################################
###################### test models #########################
############################################################

#create item (create gender, season, type)
class test_create_item(TestCase):
    #set up pre-reg for item (i.e. gender, season, type)
    def setUp(self):
        setup_items(self)

    #test is the pre-reg setup ok
    def test_item_attributes_setup(self):
        self.assertEqual(Gender_choice.objects.all().count(), 2)
        self.assertEqual(Gender_choice.objects.all()[0].name, 'female')
        self.assertEqual(Season_choice.objects.all().count(), 1)
        self.assertEqual(Season_choice.objects.all()[0].name, 'spring')
        self.assertEqual(Type_choice.objects.all().count(), 2)
        self.assertEqual(Type_choice.objects.all()[0].name, 'shirt')

    #test the item creation
    def test_item(self):
        self.assertEqual(Item.objects.all().count(),2)
        #item 1
        self.assertEqual(Item.objects.all()[0].price, 10)
        #item 2
        self.assertEqual(Item.objects.all()[1].name, 'tee1')
        self.assertEqual(Item.objects.all()[1].stock, 50)

#create users
class test_create_user(TestCase):
    def setUp(self):
        user,_ = user_create_login(self)
        self.user=user
        #this is how to add group
        admin_user = User.objects.create_user(username='shop1', password='notcustomer1')
        admin_group = Group(name = 'shop_admin')
        admin_group.save() #need to save b4 add
        admin_user.groups.add(admin_group)
        admin_user.save()
        self.admin_user = admin_user
        #every config of self have to put in setUp

    def test_login(self):
        logged_in = self.client.login(username='user1', password='password1')
        self.assertTrue(logged_in)

#create order and orderitem (create address)
class test_order_orderitem(TestCase):
    def setUp(self):
        shirt, tee = setup_items(self)
        user,_ = user_create_login(self) #_ is ignor the return value le
        orderitem1 = OrderItem(item=shirt, user=user, quantity=1)
        orderitem2 = OrderItem(item=tee, user=user, quantity=10)
        orderitem1.save()
        orderitem2.save()
        address = Address(user=user, address_line1='UK', zip_code='G1')
        address.save()
        order=Order(user=user, ship_addr=address)
        order.save()
        # orderitem3 = order.orderitems.create(item=shirt, user=user, quantity=1)
        # order.orderitems.add(OrderItem(item=shirt, user=user, quantity=1))
        order.orderitems.add(orderitem2)
        

    def test_address(self):
        self.assertEqual(Address.objects.all().count(),1)
        self.assertEqual(Address.objects.all()[0].zip_code,"G1")

    def test_orderItem(self):
        self.assertEqual(OrderItem.objects.all().count(),2)
        self.assertEqual(OrderItem.objects.all()[0].quantity,1)

    def test_order(self):
        self.assertEqual(Order.objects.all().count(),1)
        self.assertEqual(Order.objects.all()[0].ship_addr.address_line1,"UK")
        # self.assertEqual(Order.objects.all()[0].orderitems[0].name,'shirt1')


def setup_items(self):
    gender_female = Gender_choice(name="female")
    gender_female.save()
    gender_male= Gender_choice(name="male")
    gender_male.save()
    season_spring = Season_choice(name="spring")
    season_spring.save()
    type_shirt_female = Type_choice(name='shirt', product_gender=gender_female)
    type_shirt_female.save()
    type_tee_male = Type_choice(name='tee', product_gender=gender_male)
    type_tee_male.save()
    item_shirt1 = Item(name='shirt1', product_season=season_spring, product_type=type_shirt_female, 
    product_gender=gender_female, price=10, stock=100)
    item_shirt1.save()
    item_tee1 = Item(name='tee1', product_season=season_spring, product_type=type_tee_male, 
    product_gender=gender_male, price=1, stock=50, label='recom')
    item_tee1.save()
    return item_shirt1, item_tee1

def user_create(self):
    # User = get_user_model()
    user = User.objects.create_user(username='user1', password='password1')
    return user
def user_login(self):
    login = self.client.login(username='user1', password='password1')
    return login
def user_create_login(self):
    user=user_create(self)
    login = user_login(self)
    return user, login